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
            
        # Pour les actions de création (POST), on vérifie dans la BDD
        if request.method == 'POST' and not view.action == 'bulk_creer':
            matiere_id = request.data.get('matiere_id')
            if not matiere_id:
                return False
                
            try:
                matiere_repo = Container.matiere_repo()
                matiere = matiere_repo.get_by_id(matiere_id)
                # request.user.uid est le Firebase UID. enseignant_id le stocke.
                if matiere and str(matiere.enseignant_id) == str(request.user.uid):
                    return True
            except Exception as e:
                print(f"Erreur vérification permission matiere: {e}")
                
            # Fallback sur les claims au cas où
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

