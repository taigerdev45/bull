from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and \
               request.user.firebase_claims.get('role') == 'super_admin'

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and \
               request.user.firebase_claims.get('role') in ['super_admin', 'admin']

class IsSecretariat(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and \
               request.user.firebase_claims.get('role') in ['super_admin', 'admin', 'secretariat']

class IsEnseignant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and \
               request.user.firebase_claims.get('role') in ['super_admin', 'admin', 'enseignant']

class IsEtudiant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and \
               request.user.firebase_claims.get('role') == 'etudiant'
