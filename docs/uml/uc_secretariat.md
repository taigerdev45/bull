# Diagramme de Cas d'Utilisation - Secrétariat

Le secrétariat est l'acteur principal de la saisie et de la gestion quotidienne.

```mermaid
useCaseDiagram
    actor "Secrétariat" as Sec
    
    package "Gestion Académique" {
        usecase "Inscrire / Gérer les étudiants" as UC_S1
        usecase "Saisir les notes (CC/Exam/Rattrapage)" as UC_S2
        usecase "Saisir les absences" as UC_S3
        usecase "Lancer les calculs de résultats" as UC_S4
        usecase "Valider les UE et Semestres" as UC_S5
        usecase "Générer les bulletins (PDF)" as UC_S6
        usecase "Importer des données de masse (Excel)" as UC_S7
        usecase "Exporter des statistiques" as UC_S8
        
        UC_S4 ..> UC_S5 : <<precede>>
        UC_S6 ..> UC_S4 : <<include>>
    }

    Sec --> UC_S1
    Sec --> UC_S2
    Sec --> UC_S3
    Sec --> UC_S4
    Sec --> UC_S6
    Sec --> UC_S7
    Sec --> UC_S8
```
