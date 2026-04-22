# Command to grant admin role
from django.core.management.base import BaseCommand, CommandError
from infrastructure.auth.supabase_auth_service import SupabaseAuthService
from infrastructure.persistence.django_models.models import PersonnelModel

class Command(BaseCommand):
    help = 'Attribue le rôle administrateur à un utilisateur Supabase et synchronise le profil local PersonnelModel.'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email de l\'utilisateur')
        parser.add_argument('uid', type=str, help='UUID Supabase de l\'utilisateur')
        parser.add_argument('--nom', type=str, default='Admin', help='Nom de famille')
        parser.add_argument('--prenom', type=str, default='Utilisateur', help='Prénom')
        parser.add_argument('--role', type=str, default='admin', help='Rôle à attribuer')

    def handle(self, *args, **options):
        email = options['email']
        uid = options['uid']
        nom = options['nom']
        prenom = options['prenom']
        role = options['role']

        self.stdout.write(self.style.NOTICE(f"Début de la promotion pour {email} ({uid})..."))

        auth_service = SupabaseAuthService()

        # 1. Mise à jour Supabase
        try:
            self.stdout.write(f"Mise à jour des claims Supabase...")
            auth_service.set_user_claims(uid, role)
            self.stdout.write(self.style.SUCCESS("Claims Supabase mis à jour avec succès."))
        except Exception as e:
            raise CommandError(f"Erreur Supabase : {e}")

        # 2. Mise à jour Django
        try:
            self.stdout.write(f"Synchronisation de la base de données locale...")
            personnel, created = PersonnelModel.objects.update_or_create(
                user_id=uid,
                defaults={
                    "email": email,
                    "nom": nom,
                    "prenom": prenom,
                    "role": role
                }
            )
            status = "créé" if created else "mis à jour"
            self.stdout.write(self.style.SUCCESS(f"Profil Personnel {status} avec succès : {personnel}"))
        except Exception as e:
            raise CommandError(f"Erreur Django DB : {e}")

        self.stdout.write(self.style.SUCCESS(f"Opération terminée avec succès pour {email}."))
