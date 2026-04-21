# Diagramme de Cas d'Utilisation - Étudiant

L'étudiant a un accès restreint à ses propres informations en lecture seule.

```mermaid
useCaseDiagram
    actor "Étudiant" as Etu
    
    package "Espace Étudiant" {
        usecase "Consulter son profil personnel" as UC_ET1
        usecase "Consulter ses notes détaillées" as UC_ET2
        usecase "Consulter ses moyennes d'UE" as UC_ET3
        usecase "Consulter ses résultats de semestre" as UC_ET4
        usecase "Télécharger son bulletin" as UC_ET5
        usecase "Consulter son assiduité (absences)" as UC_ET6
        
        UC_ET3 ..> UC_ET2 : <<include>>
        UC_ET4 ..> UC_ET3 : <<include>>
    }

    Etu --> UC_ET1
    Etu --> UC_ET2
    Etu --> UC_ET3
    Etu --> UC_ET4
    Etu --> UC_ET5
    Etu --> UC_ET6
```
