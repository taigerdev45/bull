# Diagramme de Cas d'Utilisation - Enseignant

L'enseignant interagit principalement avec ses propres matières.

```mermaid
graph LR
    Ens((Enseignant))
    
    subgraph "Gestion des Évaluations"
        UC_E1[Consulter ses matières assignées]
        UC_E2[Consulter la liste de ses étudiants]
        UC_E3[Saisir les notes]
        UC_E4[Signaler des absences]
        UC_E5[Consulter les moyennes de sa classe]
        
        UC_E3 -.-> UC_E1 : depend
    end

    Ens --- UC_E1
    Ens --- UC_E2
    Ens --- UC_E3
    Ens --- UC_E4
    Ens --- UC_E5
```
