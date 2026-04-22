# Diagramme de Cas d'Utilisation - Étudiant

L'étudiant a un accès restreint à ses propres informations en lecture seule.

```mermaid
graph LR
    Etu((Étudiant))
    
    subgraph "Espace Étudiant"
        UC_ET1[Consulter son profil personnel]
        UC_ET2[Consulter ses notes détaillées]
        UC_ET3[Consulter ses moyennes d'UE]
        UC_ET4[Consulter ses résultats de semestre]
        UC_ET5[Télécharger son bulletin]
        UC_ET6[Consulter son assiduité (absences)]
        
        UC_ET3 -.-> UC_ET2 : include
        UC_ET4 -.-> UC_ET3 : include
    end

    Etu --- UC_ET1
    Etu --- UC_ET2
    Etu --- UC_ET3
    Etu --- UC_ET4
    Etu --- UC_ET5
    Etu --- UC_ET6
```
