from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        role = str(getattr(request.user, 'role', '')).lower().strip()
        return request.user.is_authenticated and role == 'super_admin'

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        role = str(getattr(request.user, 'role', '')).lower().strip()
        return request.user.is_authenticated and role in ['super_admin', 'admin']

class IsSecretariat(permissions.BasePermission):
    def has_permission(self, request, view):
        role = str(getattr(request.user, 'role', '')).lower().strip()
        return request.user.is_authenticated and role in ['super_admin', 'admin', 'secretariat']

class IsEnseignant(permissions.BasePermission):
    def has_permission(self, request, view):
        role = str(getattr(request.user, 'role', '')).lower().strip()
        return request.user.is_authenticated and role in ['super_admin', 'admin', 'enseignant']

class IsEtudiant(permissions.BasePermission):
    def has_permission(self, request, view):
        role = str(getattr(request.user, 'role', '')).lower().strip()
        return request.user.is_authenticated and role == 'etudiant'
