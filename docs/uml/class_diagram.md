# Diagramme de Classes (Class Diagram)

Ce diagramme représente la structure statique du domaine métier et les relations entre les entités, conformément à l'implémentation backend (Clean Architecture / DDD).

```mermaid
classDiagram
    class Etudiant {
        +String id
        +String nom
        +String prenom
        +String email
        +String matricule
        +Date date_naissance
        +String lieu_naissance
        +String bac
        +String provenance
        +String user_id
        +valider()
    }

    class Enseignant {
        +String id
        +String nom
        +String prenom
        +String email
        +String matricule
        +String user_id
        +valider()
    }

    class Personnel {
        +String id
        +String nom
        +String prenom
        +String email
        +String role
        +String user_id
        +valider()
    }

    class Semestre {
        +String id
        +String libelle
        +String annee_universitaire
    }

    class UE {
        +String id
        +String code
        +String libelle
        +int credits
        +calculerMoyennePonderee()
    }

    class Matiere {
        +String id
        +String libelle
        +float coefficient
        +int credits
        +String ue_id
        +String enseignant_id
    }

    class Evaluation {
        +String id
        +Note note
        +TypeEvaluation type
        +Date date_saisie
        +String saisie_par
        +boolean verrouille
        +modifierNote()
    }

    class Absence {
        +String id
        +float heures
        +Date date_absence
        +boolean justifiee
    }

    class Note {
        +float valeur
    }

    class Moyenne {
        +float valeur
        +Map details
    }

    Semestre "1" -- "*" UE : contient
    UE "1" -- "*" Matiere : compose
    Matiere "1" -- "*" Evaluation : evaluee_par
    Etudiant "1" -- "*" Evaluation : obtient
    Etudiant "1" -- "*" Absence : a
    Matiere "*" -- "0..1" Enseignant : enseigne_par
    
    Evaluation ..> Note : utilise
    UE ..> Moyenne : produit
```
