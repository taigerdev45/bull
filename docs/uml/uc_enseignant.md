# Diagramme de Cas d'Utilisation - Enseignant

L'enseignant interagit principalement avec ses propres matières.

```mermaid
useCaseDiagram
    actor "Enseignant" as Ens
    
    package "Gestion des Évaluations" {
        usecase "Consulter ses matières assignées" as UC_E1
        usecase "Consulter la liste de ses étudiants" as UC_E2
        usecase "Saisir les notes de ses matières" as UC_E3
        usecase "Signaler des absences" as UC_E4
        usecase "Consulter les moyennes de sa classe" as UC_E5
        
        UC_E3 ..> UC_E1 : <<depend>>
    }

    Ens --> UC_E1
    Ens --> UC_E2
    Ens --> UC_E3
    Ens --> UC_E4
    Ens --> UC_E5
```
