import sys
import os
import django
from datetime import date

# Configuration de Django
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from infrastructure.persistence.django_models.models import (
    EtudiantModel, EnseignantModel, SemestreModel, UEModel, 
    MatiereModel, EvaluationModel, AbsenceModel
)

def seed():
    print("START: Peuplement de la base de données...")

    # 1. Semestres
    s5, _ = SemestreModel.objects.get_or_create(id='S5', defaults={'libelle': 'Semestre 5'})
    s6, _ = SemestreModel.objects.get_or_create(id='S6', defaults={'libelle': 'Semestre 6'})

    # 2. UE
    ue_asur, _ = UEModel.objects.get_or_create(
        code='UE11_ASUR', 
        defaults={'libelle': 'Administration Systèmes et Réseaux', 'credits': 6, 'semestre': s5}
    )
    ue_dev, _ = UEModel.objects.get_or_create(
        code='UE12_DEV', 
        defaults={'libelle': 'Développement Application', 'credits': 4, 'semestre': s5}
    )

    # 3. Enseignants
    prof_turing, _ = EnseignantModel.objects.get_or_create(
        email='turing@example.com',
        defaults={'nom': 'Turing', 'prenom': 'Alan', 'matricule': 'ENS001'}
    )
    prof_lovelace, _ = EnseignantModel.objects.get_or_create(
        email='lovelace@example.com',
        defaults={'nom': 'Lovelace', 'prenom': 'Ada', 'matricule': 'ENS002'}
    )

    # 4. Matières
    linux, _ = MatiereModel.objects.get_or_create(
        libelle='Système Linux',
        defaults={'coefficient': 2.0, 'credits': 3, 'ue': ue_asur, 'enseignant': prof_turing}
    )
    python, _ = MatiereModel.objects.get_or_create(
        libelle='Programmation Python',
        defaults={'coefficient': 1.5, 'credits': 2, 'ue': ue_dev, 'enseignant': prof_lovelace}
    )

    # 5. Étudiants
    students_data = [
        ('Jean', 'Dupont', 'stu@example.com', 'MAT001'),
        ('Marie', 'Curie', 'marie@example.com', 'MAT002'),
        ('Albert', 'Einstein', 'albert@example.com', 'MAT003'),
    ]
    
    students = []
    for prenom, nom, email, mat in students_data:
        s, _ = EtudiantModel.objects.get_or_create(
            email=email,
            defaults={
                'nom': nom, 
                'prenom': prenom, 
                'matricule': mat, 
                'date_naissance': date(2000, 1, 1),
                'user_id': f'fake_uid_{mat}'
            }
        )
        students.append(s)

    # 6. Évaluations (Notes)
    for s in students:
        EvaluationModel.objects.get_or_create(
            etudiant=s,
            matiere=linux,
            type='CC',
            defaults={'note': 12.5 if s.nom == 'Dupont' else 15.0}
        )
        EvaluationModel.objects.get_or_create(
            etudiant=s,
            matiere=python,
            type='EXAMEN',
            defaults={'note': 14.0 if s.nom == 'Curie' else 11.5}
        )

    # 7. Absences
    for s in students[:2]:
        AbsenceModel.objects.get_or_create(
            etudiant=s,
            matiere=linux,
            date_absence=date.today(),
            defaults={'heures': 2.0, 'justifiee': False}
        )

    print("DONE: Base de données peuplée avec succès !")

if __name__ == '__main__':
    seed()
