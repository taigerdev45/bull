import firebase_admin.auth
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

class FirebaseAuthentication(authentication.BaseAuthentication):
    """Système d'authentification personnalisée basé sur Firebase JWT."""

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None

        id_token = auth_header.split(' ').pop()
        try:
            # 1. Vérification du token via Firebase Admin SDK
            decoded_token = firebase_admin.auth.verify_id_token(id_token)
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Token Firebase invalide: {str(e)}')

        uid = decoded_token.get('uid')
        if not uid:
            raise exceptions.AuthenticationFailed('UID Firebase manquant dans le token.')

        # 2. Récupération ou création de l'utilisateur Django local
        user, created = User.objects.get_or_create(username=uid)
        
        # 3. Stockage des infos Firebase dans l'objet user pour les permissions (Custom Claims)
        user.firebase_claims = decoded_token 
        
        return (user, None)
