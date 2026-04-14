from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and \
               request.user.firebase_claims.get('role') == 'admin'

class IsSecretariat(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and \
               request.user.firebase_claims.get('role') in ['admin', 'secretariat']

class IsEnseignant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and \
               request.user.firebase_claims.get('role') in ['admin', 'enseignant']

class IsEtudiant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and \
               request.user.firebase_claims.get('role') == 'etudiant'
