# Diagramme de Classes (Class Diagram)

Ce diagramme représente la structure statique du domaine métier et les relations entre les entités.

```mermaid
classDiagram
    class Etudiant {
        -String id
        +String nom
        +String prenom
        +String email
        +String matricule
        +Date date_naissance
        +valider()
    }

    class Enseignant {
        -String id
        +String nom
        +String prenom
        +String email
        +String matricule
        +valider()
    }

    class Semestre {
        -String id
        +String libelle
        +valider()
    }

    class UE {
        -String id
        +String code
        +String libelle
        +int credits
        +float moyenne_min
        +calculerMoyenne()
        +validerUE()
    }

    class Matiere {
        -String id
        +String libelle
        +float coefficient
        +int credits
        +float calculerMoyenneMatiere()
    }

    class Evaluation {
        -String id
        +float note
        +String type
        +Date date_evaluation
        +verifierNote()
    }

    class Absence {
        -String id
        +float heures
        +Date date_absence
        +boolean justifiee
    }

    class ResultatUE {
        -String etudiant_id
        -String ue_id
        +Moyenne moyenne
        +appliquerCompensation()
    }

    class ResultatSemestre {
        -String etudiant_id
        +int semestre
        +Moyenne moyenne
    }

    class ResultatAnnuel {
        -String etudiant_id
        +String annee_academique
        +Moyenne moyenne
        +determinerMention()
    }

    Semestre "1" -- "*" UE : contient
    UE "1" -- "*" Matiere : compose
    Matiere "1" -- "*" Evaluation : est evaluee par
    Etudiant "1" -- "*" Evaluation : obtient
    Etudiant "1" -- "*" Absence : a
    Matiere "*" -- "0..1" Enseignant : est enseignée par
    
    Etudiant "1" -- "*" ResultatUE : possède
    UE "1" -- "*" ResultatUE : concerne
    Etudiant "1" -- "*" ResultatSemestre : possède
    Etudiant "1" -- "*" ResultatAnnuel : possède
```
