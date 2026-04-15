from django.core.management.base import BaseCommand
from dependency_injector.wiring import inject, Provide
from infrastructure.config.dependency_injection import Container

class Command(BaseCommand):
    help = 'Vérifier l\'intégrité des calculs pour un étudiant.'

    def add_arguments(self, parser):
        parser.add_argument('--etudiant-id', type=str, required=True, help='Matricule de l\'étudiant')

    @inject
    def handle(self, *args, **options):
        container = Container()
        resultat_repo = container.resultat_repo()
        orchestre_calcul = container.orchestre_calcul()
        etudiant_id = options['etudiant_id']

        self.stdout.write(f"🔍 Audit des calculs pour {etudiant_id}...")

        # 1. Récupérer données actuelles
        res_current = resultat_repo.obtenir_par_etudiant_semestre(etudiant_id, "S5")
        
        # 2. Lancer un recalcul forcé
        # On suppose que orchestrateur.calculer_bulletin_semestre renvoie les données calculées
        # Note: on a besoin des données de structure pour appeler calculer_bulletin_semestre
        # Pour simplifier dans cette commande CLI, on compare le résultat stocké 
        # après avoir appelé recalculer_pour_etudiant
        
        old_moyenne = res_current.moyenne_generale if res_current else 0
        orchestre_calcul.recalculer_pour_etudiant(etudiant_id)
        new_res = resultat_repo.obtenir_par_etudiant_semestre(etudiant_id, "S5")
        new_moyenne = new_res.moyenne_generale if new_res else 0

        self.stdout.write(f"  Moyenne stockée : {old_moyenne}")
        self.stdout.write(f"  Moyenne recalculée : {new_moyenne}")

        if abs(old_moyenne - new_moyenne) < 0.001:
            self.stdout.write(self.style.SUCCESS("✅ Intégrité vérifiée : Aucune divergence détectée."))
        else:
            self.stdout.write(self.style.ERROR(f"❌ ÉCART DÉTECTÉ : {abs(old_moyenne - new_moyenne)}"))
