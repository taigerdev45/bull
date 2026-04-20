from dataclasses import dataclass
from typing import List, Dict

@dataclass(frozen=True)
class MatiereConfig:
    libelle: str
    coefficient: int
    credits: int

@dataclass(frozen=True)
class UEConfig:
    code: str
    libelle: str
    credits: int
    matieres: List[MatiereConfig]

@dataclass(frozen=True)
class SemestreConfig:
    libelle: str
    total_credits: int
    ues: List[UEConfig]

# DONNÉES EXACTES CAHIER DES CHARGES
REFERENTIEL_LP_ASUR: Dict[str, SemestreConfig] = {
    'S5': SemestreConfig(
        libelle='Semestre 5',
        total_credits=30,
        ues=[
            UEConfig(
                code='UE5-1',
                libelle='Enseignement Général',
                credits=11,
                matieres=[
                    MatiereConfig('Anglais technique', 1, 2),
                    MatiereConfig("Management d'équipe", 1, 1),
                    MatiereConfig('Communication', 2, 1),
                    MatiereConfig("Droit de l'informatique", 2, 2),
                    MatiereConfig('Gestion de projets', 1, 1),
                    MatiereConfig('Veille technologique', 1, 1),
                    MatiereConfig('Consolidation bases de la programmation', 2, 2),
                    MatiereConfig('Conception BDD et SQL', 2, 2),
                ]
            ),
            UEConfig(
                code='UE5-2',
                libelle='Connaissances de Base et Outils pour les Réseaux d\'Entreprise',
                credits=19,
                matieres=[
                    MatiereConfig('Remise à niveau IOS', 2, 2),
                    MatiereConfig('Connaissance des réseaux LAN', 2, 2),
                    MatiereConfig('Les langages du script', 2, 2),
                    MatiereConfig('Virtualisation', 3, 3),
                    MatiereConfig('Application client-serveur', 2, 2),
                    MatiereConfig('Téléphonie IP avancée', 2, 2),
                    MatiereConfig('Services à valeur ajoutée', 2, 2),
                    MatiereConfig('CCNA2', 1, 2),
                ]
            )
        ]
    ),
    'S6': SemestreConfig(
        libelle='Semestre 6',
        total_credits=30,
        ues=[
            UEConfig(
                code='UE6-1',
                libelle='Sciences de Base',
                credits=20,
                matieres=[
                    MatiereConfig('Environnement Windows', 3, 3),
                    MatiereConfig('Environnement Linux', 3, 3),
                    MatiereConfig('Interopérabilité', 3, 3),
                    MatiereConfig('Cryptage et Authentification', 2, 2),
                    MatiereConfig('Prévention et Sécurité', 3, 3),
                    MatiereConfig('Optimisation de l\'accès Internet', 3, 3),
                    MatiereConfig('Contrôle d\'accès distant', 2, 2),
                    MatiereConfig('CCNA3', 1, 1),
                ]
            ),
            UEConfig(
                code='UE6-2',
                libelle='Télécommunications et Réseaux',
                credits=10,
                matieres=[
                    MatiereConfig('Méthodologie de rédaction du rapport de stage', 2, 2),
                    MatiereConfig('Soutenance', 8, 8),
                ]
            )
        ]
    )
}

# Seuils académiques
SEUIL_VALIDATION_UE = 10.0
SEUIL_VALIDATION_SEMESTRE_CREDITS = 30
SEUIL_VALIDATION_ANNEE_CREDITS = 60

# Mentions
MENTIONS = [
    (16.0, 20.0, 'TRES_BIEN'),
    (14.0, 16.0, 'BIEN'),
    (12.0, 14.0, 'ASSEZ_BIEN'),
    (10.0, 12.0, 'PASSABLE'),
]

# Paramètres de calcul (non spécifiés dans le snippet mais maintenus pour la logique globale)
PONDERATION_CC = 0.4
PONDERATION_EXAMEN = 0.6
PENALITE_PAR_HEURE = 0.01

# Seuils académiques additionnels
CREDITS_SEMESTRE = 30
MENTION_PASSABLE = 10.0
MENTION_ASSEZ_BIEN = 12.0
MENTION_BIEN = 14.0
MENTION_TRES_BIEN = 16.0
