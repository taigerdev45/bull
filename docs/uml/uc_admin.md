# Diagramme de Cas d'Utilisation - Administrateur

Focus sur les responsabilités de l'administrateur système.

```mermaid
useCaseDiagram
    actor "Administrateur" as Admin
    
    package "Administration Système" {
        usecase "Créer des comptes personnels (Admin/Sec)" as UC_A1
        usecase "Gérer les comptes enseignants" as UC_A2
        usecase "Assigner des rôles et permissions" as UC_A3
        usecase "Configurer les paramètres académiques" as UC_A4
        usecase "Consulter les logs d'audit" as UC_A5
        usecase "Gérer les UE et Semestres" as UC_A6
        
        UC_A1 ..> UC_A3 : <<include>>
        UC_A2 ..> UC_A3 : <<include>>
    }

    Admin --> UC_A1
    Admin --> UC_A2
    Admin --> UC_A4
    Admin --> UC_A5
    Admin --> UC_A6
```
