from django.core.management.base import BaseCommand
from infrastructure.persistence.firebase.connection import FirebaseConnection
from infrastructure.config.constants import REFERENTIEL_LP_ASUR

class Command(BaseCommand):
    help = 'Initialise le référentiel académique (Semestres, UEs, Matières) dans Firestore.'

    def handle(self, *args, **options):
        connection = FirebaseConnection()
        db = connection.client
        
        referentiel = REFERENTIEL_LP_ASUR
        
        print("Initialisation du referentiel...")
        
        for semestre in referentiel.values():
            print(f"--- {semestre.libelle} ---")
            
            for ue in semestre.ues:
                ue_ref = db.collection('ues').document(ue.code)
                
                # Mise à jour forcée pour normaliser le schéma
                print(f"  [MAJ] UE {ue.code}")
                
                # Extraction de l'index du semestre (ex: "Semestre 5" -> 5)
                import re
                match = re.search(r'\d+', semestre.libelle)
                s_id = int(match.group()) if match else semestre.libelle
                
                ue_ref.set({
                    'code': ue.code,
                    'libelle': ue.libelle,
                    'credits': ue.credits,
                    'semestre_id': s_id,
                    'matieres_ids': [m.libelle.replace(" ", "_").lower() for m in ue.matieres]
                })

                for matiere in ue.matieres:
                    m_id = matiere.libelle.replace(" ", "_").lower()
                    matiere_ref = db.collection('matieres').document(m_id)
                    
                    if not matiere_ref.get().exists:
                        print(f"    [Création] Matière {matiere.libelle}")
                        matiere_ref.set({
                            'id': m_id,
                            'libelle': matiere.libelle,
                            'coefficient': matiere.coefficient,
                            'ue_id': ue.code
                        })
                    else:
                        print(f"    [Saut] Matière {matiere.libelle} existe déjà.")

        print("Referentiel initialise avec succes !")
