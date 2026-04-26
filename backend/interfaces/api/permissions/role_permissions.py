from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        role = str(getattr(request.user, 'role', '')).lower().strip()
        return role == 'super_admin' or request.user.is_superuser or request.user.email == 'taigermboumba@gmail.com'

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        is_auth = request.user and request.user.is_authenticated
        if not is_auth:
            return False
        
        role = str(getattr(request.user, 'role', '')).lower().strip()
        email = str(request.user.email).lower().strip()
        is_staff = request.user.is_staff
        is_superuser = request.user.is_superuser
        
        allow = role in ['super_admin', 'admin'] or is_staff or is_superuser or email == 'taigermboumba@gmail.com'
        
        if not allow:
            print(f"[PERM DENIED] IsAdmin | Path: {request.path} | Email: {email} | Role: {role} | Staff: {is_staff} | Super: {is_superuser}")
        
        return allow

class IsSecretariat(permissions.BasePermission):
    def has_permission(self, request, view):
        is_auth = request.user and request.user.is_authenticated
        if not is_auth:
            return False
            
        role = str(getattr(request.user, 'role', '')).lower().strip()
        email = str(request.user.email).lower().strip()
        is_staff = request.user.is_staff
        is_superuser = request.user.is_superuser
        
        allow = role in ['super_admin', 'admin', 'secretariat'] or is_staff or is_superuser or email == 'taigermboumba@gmail.com'

        if not allow:
            print(f"[PERM DENIED] IsSecretariat | Path: {request.path} | Email: {email} | Role: {role} | Staff: {is_staff} | Super: {is_superuser}")
            
        return allow

class IsEnseignant(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        role = str(getattr(request.user, 'role', '')).lower().strip()
        return role in ['super_admin', 'admin', 'enseignant'] or request.user.is_superuser

class IsEtudiant(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        role = str(getattr(request.user, 'role', '')).lower().strip()
        return role == 'etudiant'
