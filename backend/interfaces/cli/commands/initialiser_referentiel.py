import os
import django
from infrastructure.persistence.firebase.connection import FirebaseConnection
from infrastructure.config.constants import REFERENTIEL_LP_ASUR

def run():
    """Initialise le référentiel LP ASUR dans Firestore."""
    print("🚀 Initialisation du référentiel pédagogique LP ASUR...")
    
    connection = FirebaseConnection()
    db = connection.client
    
    for semestre in REFERENTIEL_LP_ASUR.values():
        print(f"--- {semestre.libelle} ---")
        
        for ue in semestre.ues:
            # Idempotence: vérification de l'existence de l'UE
            ue_ref = db.collection('ues').document(ue.code)
            if ue_ref.get().exists:
                print(f"  [Saut] UE {ue.code} existe déjà.")
            else:
                print(f"  [Création] UE {ue.code}: {ue.libelle}")
                ue_ref.set({
                    'code': ue.code,
                    'libelle': ue.libelle,
                    'credits': ue.credits,
                    'semestre': semestre.libelle,
                    'matieres_ids': [m.libelle.replace(" ", "_").lower() for m in ue.matieres]
                })

            for matiere in ue.matieres:
                m_id = matiere.libelle.replace(" ", "_").lower()
                m_ref = db.collection('matieres').document(m_id)
                
                if m_ref.get().exists:
                    print(f"    [Saut] Matière {matiere.libelle} existe déjà.")
                else:
                    print(f"    [Création] Matière: {matiere.libelle} (Coeff: {matiere.coefficient})")
                    m_ref.set({
                        'libelle': matiere.libelle,
                        'coefficient': matiere.coefficient,
                        'credits': matiere.credits,
                        'ue_id': ue.code
                    })

    print("✅ Référentiel initialisé avec succès !")

if __name__ == "__main__":
    # Setup environnement Django si exécuté directement
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    run()
