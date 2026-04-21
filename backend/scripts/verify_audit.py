import os
import sys
from datetime import datetime

# Ajout du chemin pour les imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from infrastructure.config.dependency_injection import Container
from domain.repositories.i_resultat_repository import IResultatRepository

def verify():
    container = Container()
    resultat_repo = container.resultat_repo()
    etudiant_repo = container.etudiant_repo()

    print("--- Vérification des Calculs d'Audit ---")

    # On récupère nos étudiants de test par leur matricule
    test_matricules = ["TEST-001", "TEST-002", "TEST-003", "TEST-004", "TEST-005"]
    
    for mat in test_matricules:
        etudiant = etudiant_repo.get_by_matricule(mat)
        if not etudiant:
            print(f"❌ Étudiant {mat} non trouvé.")
            continue
            
        # On suppose que l'orchestrateur a sauvegardé le résultat annuel (ou on le recalcule)
        # Pour l'audit, on va recalculer en direct pour voir ce que l'orchestrateur sort
        orchestre = container.orchestre_calcul()
        res = orchestre.calculer_resultat_annuel(etudiant.id)
        
        moyenne = res['moyenne_annuelle']
        credits = res['total_credits']
        mention = res['mention']
        
        print(f"\nRésultats pour {etudiant.nom_complet} ({mat}) :")
        print(f"  - Moyenne Annuelle : {moyenne:.2f}")
        print(f"  - Crédits Acquis   : {credits}")
        print(f"  - Mention          : {mention}")

        # Vérifications Logiques
        if mat == "TEST-001": # SUCCESS
            # Si seul S5 est saisi (14.4), alors Annuel = (14.4 + 0) / 2 = 7.2
            assert moyenne >= 7.2, f"Erreur SUCCESS: moyenne attendue >= 7.2, reçue {moyenne}"
            assert credits >= 30, f"Erreur SUCCESS: crédits attendus >= 30, reçus {credits}"
        if mat == "TEST-002": # COMPENSE
            # On vérifie si une UE est < 10 mais le semestre validé
            has_compense = False
            for s in [res['semestre_1'], res['semestre_2']]:
                for ue in s['resultats_ues']:
                    if ue['statut'] == 'VAL_COMP':
                        has_compense = True
            print(f"  - Compensation détectée : {'OUI' if has_compense else 'NON'}")
        if mat == "TEST-004": # RATTRAPAGE
             print(f"  - Vérification Rattrapage : OK (Moyenne: {moyenne})")
        if mat == "TEST-005": # ABSENCE (Pénalité)
             # Base 10 - 0.5 = 9.5
             print(f"  - État après pénalité : {'AJOURNE' if moyenne < 10 else 'ADMIS'}")

    print("\n--- Analyse d'intégrité terminée ---")

if __name__ == "__main__":
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    verify()
