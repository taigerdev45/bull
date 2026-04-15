from django.core.management.base import BaseCommand
from dependency_injector.wiring import inject, Provide
from infrastructure.config.dependency_injection import Container

class Command(BaseCommand):
    help = 'Recalcule les moyennes de tous les étudiants d\'une promotion.'

    def add_arguments(self, parser):
        parser.add_argument('promotion', type=str, help='Nom de la promotion (ex: 2026)')

    @inject
    def handle(self, *args, **options):
        container = Container()
        etudiant_repo = container.etudiant_repo()
        orchestre_calcul = container.orchestre_calcul()
        promotion = options['promotion']

        self.stdout.write(f"🔄 Début du recalcul pour la promotion {promotion}...")

        etudiants = etudiant_repo.list_all()
        etudiants_promo = [e for e in etudiants if e.promotion == promotion]

        if not etudiants_promo:
            self.stdout.write(self.style.WARNING(f"Aucun étudiant trouvé pour la promotion {promotion}."))
            return

        succes = 0
        erreurs = 0

        for etudiant in etudiants_promo:
            try:
                self.stdout.write(f"  - Calcul pour {etudiant.nom} {etudiant.prenom} ({etudiant.matricule})")
                orchestre_calcul.recalculer_pour_etudiant(etudiant.matricule)
                succes += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ❌ Erreur pour {etudiant.matricule}: {str(e)}"))
                erreurs += 1

        self.stdout.write(self.style.SUCCESS(f"\n✅ Recalcul terminé : {succes} succès, {erreurs} erreurs."))
