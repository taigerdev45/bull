import os
import random
from typing import List
from django.core.management.base import BaseCommand
from dependency_injector.wiring import inject, Provide
from infrastructure.config.dependency_injection import Container
from domain.entities.etudiant import Etudiant
from domain.entities.evaluation import Evaluation, TypeEvaluation
from domain.value_objects.note import Note
from domain.value_objects.coefficient import Coefficient
from openpyxl import Workbook

class Command(BaseCommand):
    help = 'Génère 24 étudiants de test avec des données réalistes.'

    @inject
    def handle(self, *args, **options):
        container = Container()
        etudiant_repo = container.etudiant_repo()
        matiere_repo = container.matiere_repo()
        evaluation_repo = container.evaluation_repo()

        self.stdout.write(self.style.SUCCESS('🚀 Début de la génération du jeu de test...'))

        matieres = matiere_repo.list_all()
        if not matieres:
            self.stdout.write(self.style.ERROR('Erreur: Aucun référentiel (matières) trouvé. Lancez initialiser_referentiel d\'abord.'))
            return

        wb = Workbook()
        ws = wb.active
        ws.title = "Jeu de Test - Référence"
        ws.append(["Matricule", "Nom", "Prénom", "Matière", "Type", "Note", "Profil Attendu"])

        noms = ["TRAORE", "DIARRA", "KOULIBALY", "SISSOKO", "CAMARA", "KEITA", "TOURE", "BATHILY"]
        prenoms = ["Moussa", "Fatou", "Amadou", "Awa", "Ibrahim", "Mariam", "Sekou", "Oumou"]

        for i in range(1, 25):
            matricule = f"TEST{2026}{i:03d}"
            nom = random.choice(noms)
            prenom = random.choice(prenoms)
            
            etudiant = Etudiant(matricule=matricule, nom=nom, prenom=prenom, promotion="2026")
            etudiant_repo.save(etudiant)

            # Définition du profil de réussite
            if i <= 5: profil = "EXCELLENT"
            elif i <= 15: profil = "MOYEN"
            elif i <= 20: profil = "COMPENSATION"
            else: profil = "ECHEC"

            for matiere in matieres:
                # Génération de notes selon le profil
                base_note = self._generer_note_par_profil(profil)
                
                # Saisie CC et EXAMEN
                for type_ev in [TypeEvaluation.CC, TypeEvaluation.EXAMEN]:
                    note_val = min(20, max(0, base_note + random.uniform(-2, 2)))
                    eval_obj = Evaluation(
                        etudiant_id=matricule,
                        matiere_id=matiere.id,
                        type=type_ev,
                        note=Note(round(note_val, 2)),
                        saisie_par="SYSTEM_SETUP"
                    )
                    evaluation_repo.creer(eval_obj)
                    ws.append([matricule, nom, prenom, matiere._libelle, type_ev.name, eval_obj.note.valeur, profil])

        file_path = "tests/reference_jeu_test_24.xlsx"
        os.makedirs("tests", exist_ok=True)
        wb.save(file_path)
        
        self.stdout.write(self.style.SUCCESS(f'✓ 24 étudiants générés avec succès.'))
        self.stdout.write(self.style.SUCCESS(f'✓ Fichier de référence créé : {file_path}'))

    def _generer_note_par_profil(self, profil: str) -> float:
        if profil == "EXCELLENT": return random.uniform(15, 18)
        if profil == "MOYEN": return random.uniform(11, 14)
        if profil == "COMPENSATION": return random.uniform(8, 10)
        return random.uniform(4, 7)
