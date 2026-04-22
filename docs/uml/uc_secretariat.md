# Diagramme de Cas d'Utilisation - Secrétariat

Le secrétariat est l'acteur principal de la saisie et de la gestion quotidienne.

```mermaid
graph LR
    Sec((Secrétariat))
    
    subgraph "Gestion Académique"
        UC_S1[Inscrire / Gérer les étudiants]
        UC_S2[Saisir les notes CC/Exam/Rattrapage]
        UC_S3[Saisir les absences]
        UC_S4[Lancer les calculs de résultats]
        UC_S5[Valider les UE et Semestres]
        UC_S6[Générer les bulletins PDF]
        UC_S7[Importer données de masse Excel]
        UC_S8[Exporter des statistiques]
        
        UC_S4 -.-> UC_S5 : precede
        UC_S6 -.-> UC_S4 : include
    end

    Sec --- UC_S1
    Sec --- UC_S2
    Sec --- UC_S3
    Sec --- UC_S4
    Sec --- UC_S6
    Sec --- UC_S7
    Sec --- UC_S8
```
