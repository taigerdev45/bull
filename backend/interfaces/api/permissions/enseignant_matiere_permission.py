from rest_framework import permissions
from infrastructure.config.dependency_injection import Container

class IsEnseignantMatiere(permissions.BasePermission):
    """
    Vérifie que l'enseignant a le droit de saisir des notes pour la matière spécifiée.
    La vérification se base maintenant sur la base de données pour éviter les problèmes 
    de synchronisation des custom claims Firebase sur Render.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        role = getattr(request.user, 'role', request.user.firebase_claims.get('role'))
        if role in ['admin', 'super_admin', 'secretariat']:
            return True
            
        if role != 'enseignant':
            return False
            
        # Pour les actions de création (POST)
        if request.method == 'POST':
            matiere_id = request.data.get('matiere_id')
            
            # Si c'est un bulk, on peut avoir la matiere_id à la racine ou dans chaque item
            # Pour la permission globale has_permission, on vérifie au moins la matiere_id racine si présente
            if not matiere_id and view.action == 'bulk_creer':
                evals = request.data.get('evaluations', [])
                if evals and isinstance(evals, list):
                    matiere_id = evals[0].get('matiere_id')

            if not matiere_id:
                return view.action == 'bulk_creer' # Autorise si bulk sans matiere racine (le handler filtrera si besoin)
                
            try:
                from infrastructure.persistence.django_models.models import MatiereModel
                # On cherche la matière par ID ou Code
                m_query = MatiereModel.objects.filter(id=matiere_id) | MatiereModel.objects.filter(code=matiere_id)
                m_model = m_query.first()
                
                if m_model and m_model.enseignant and str(m_model.enseignant.user_id) == str(request.user.uid):
                    return True
            except Exception as e:
                print(f"Erreur vérification permission matiere: {e}")
                
            # Fallback sur les claims
            matieres_autorisees = request.user.firebase_claims.get('matieres', [])
            return str(matiere_id) in [str(m) for m in matieres_autorisees]
            
        return True

    def has_object_permission(self, request, view, obj):
        role = getattr(request.user, 'role', request.user.firebase_claims.get('role'))
        if role in ['admin', 'super_admin', 'secretariat']:
            return True
        
        try:
            matiere_repo = Container.matiere_repo()
            matiere = matiere_repo.get_by_id(obj.matiere_id)
            if matiere and str(matiere.enseignant_id) == str(request.user.uid):
                return True
        except Exception:
            pass
            
        matieres_autorisees = request.user.firebase_claims.get('matieres', [])
        return str(obj.matiere_id) in [str(m) for m in matieres_autorisees]

