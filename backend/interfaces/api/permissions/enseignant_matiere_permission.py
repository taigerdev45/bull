from rest_framework import permissions

class IsEnseignantMatiere(permissions.BasePermission):
    """
    Vérifie que l'enseignant a le droit de saisir des notes pour la matière spécifiée.
    La vérification se base sur les custom claims 'matieres' du token Firebase.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        role = request.user.firebase_claims.get('role')
        if role == 'admin':
            return True
            
        if role != 'enseignant':
            return False
            
        # Pour les actions de création (POST), on vérifie le body
        if request.method == 'POST' and not view.action == 'bulk_creer':
            matiere_id = request.data.get('matiere_id')
            matieres_autorisees = request.user.firebase_claims.get('matieres', [])
            return matiere_id in matieres_autorisees
            
        return True

    def has_object_permission(self, request, view, obj):
        role = request.user.firebase_claims.get('role')
        if role == 'admin':
            return True
        
        # Pour les objets existants (Evaluation), on vérifie sa matiere_id
        matieres_autorisees = request.user.firebase_claims.get('matieres', [])
        return obj.matiere_id in matieres_autorisees
