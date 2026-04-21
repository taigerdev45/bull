import os
import sys
from datetime import datetime

# Ajout du chemin pour les imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from infrastructure.config.dependency_injection import Container
from domain.entities.etudiant import Etudiant
from domain.entities.evaluation import Evaluation, TypeEvaluation
from domain.entities.absence import Absence
from domain.value_objects.note import Note

def seed():
    container = Container()
    
    # Repositories
    etudiant_repo = container.etudiant_repo()
    evaluation_repo = container.evaluation_repo()
    matiere_repo = container.matiere_repo()
    absence_repo = container.absence_repo()
    orchestre = container.orchestre_calcul()

    print("--- Début du Seeding de Test ---")

    # 1. Création des Étudiants de Test
    scenarios = [
        {"nom": "SUCCESS", "prenom": "Direct", "matricule": "TEST-001", "email": "success@test.com"},
        {"nom": "COMPENSE", "prenom": "Jean", "matricule": "TEST-002", "email": "compense@test.com"},
        {"nom": "ECHEC", "prenom": "Paul", "matricule": "TEST-003", "email": "echec@test.com"},
        {"nom": "RATTRAPAGE", "prenom": "Marie", "matricule": "TEST-004", "email": "rattrapage@test.com"},
        {"nom": "ABSENT", "prenom": "Luc", "matricule": "TEST-005", "email": "absent@test.com"}
    ]

    etu_ids = {}
    for s in scenarios:
        etudiant = Etudiant(
            nom=s["nom"], 
            prenom=s["prenom"], 
            matricule=s["matricule"], 
            email=s["email"],
            date_naissance=datetime(2000, 1, 1).date()
        )
        etudiant_repo.save(etudiant)
        etu_ids[s["nom"]] = etudiant.id
        print(f"Étudiant créé : {s['nom']} (ID: {etudiant.id})")

    # Récupération d'une matière (ex: UE5-1 M1)
    # On assume que le référentiel est déjà initialisé via 'python manage.py initialiser_referentiel'
    matieres = matiere_repo.list_all()
    if not matieres:
        print("Erreur: Référentiel non initialisé. Lancez 'initialiser_referentiel' d'abord.")
        return
    
    m1 = matieres[0] # Première matière
    m2 = matieres[1] if len(matieres) > 1 else m1 # Deuxième matière

    # 2. Application des scénarios de notes
    
    # SCENARIO: SUCCESS DIRECT (15 en CC, 14 en Examen)
    evaluation_repo.creer(Evaluation(etu_ids["SUCCESS"], m1.id, TypeEvaluation.CC, Note(15.0), "SEEDER"))
    evaluation_repo.creer(Evaluation(etu_ids["SUCCESS"], m1.id, TypeEvaluation.EXAMEN, Note(14.0), "SEEDER"))

    # SCENARIO: COMPENSE (UE1: 8.0, UE2: 12.0 -> Moyenne 10.0)
    # Matière 1 (échec)
    evaluation_repo.creer(Evaluation(etu_ids["COMPENSE"], m1.id, TypeEvaluation.CC, Note(8.0), "SEEDER"))
    evaluation_repo.creer(Evaluation(etu_ids["COMPENSE"], m1.id, TypeEvaluation.EXAMEN, Note(8.0), "SEEDER"))
    # Matière 2 (succès qui compense)
    evaluation_repo.creer(Evaluation(etu_ids["COMPENSE"], m2.id, TypeEvaluation.CC, Note(12.0), "SEEDER"))
    evaluation_repo.creer(Evaluation(etu_ids["COMPENSE"], m2.id, TypeEvaluation.EXAMEN, Note(12.0), "SEEDER"))

    # SCENARIO: ECHEC (Moyenne 5.0)
    evaluation_repo.creer(Evaluation(etu_ids["ECHEC"], m1.id, TypeEvaluation.CC, Note(5.0), "SEEDER"))
    evaluation_repo.creer(Evaluation(etu_ids["ECHEC"], m1.id, TypeEvaluation.EXAMEN, Note(5.0), "SEEDER"))

    # SCENARIO: RATTRAPAGE (CC: 4, EX: 6 -> RAT: 12)
    evaluation_repo.creer(Evaluation(etu_ids["RATTRAPAGE"], m1.id, TypeEvaluation.CC, Note(4.0), "SEEDER"))
    evaluation_repo.creer(Evaluation(etu_ids["RATTRAPAGE"], m1.id, TypeEvaluation.EXAMEN, Note(6.0), "SEEDER"))
    evaluation_repo.creer(Evaluation(etu_ids["RATTRAPAGE"], m1.id, TypeEvaluation.RATTRAPAGE, Note(12.0), "SEEDER"))

    # SCENARIO: ABSENT (CC: 10, EX: 10, 50h d'absences -> 10 - 0.5 = 9.5)
    evaluation_repo.creer(Evaluation(etu_ids["ABSENT"], m1.id, TypeEvaluation.CC, Note(10.0), "SEEDER"))
    evaluation_repo.creer(Evaluation(etu_ids["ABSENT"], m1.id, TypeEvaluation.EXAMEN, Note(10.0), "SEEDER"))
    absence_repo.creer(Absence(etu_ids["ABSENT"], m1.id, 50, datetime.now().date(), "SEEDER"))

    print("\n--- Recalcul Global ---")
    for nom, eid in etu_ids.items():
        orchestre.calculer_resultat_annuel(eid)
        print(f"Calcul terminé pour {nom}")

    print("\n--- Seeding Terminé avec succès ---")

if __name__ == "__main__":
    # Setup environnement Django si exécuté directement
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    seed()
