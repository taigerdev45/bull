# Diagramme de Cas d'Utilisation - Administrateur

Focus sur les responsabilités de l'administrateur système.

```mermaid
graph LR
    Admin((Administrateur))

    subgraph "Administration Système"
        UC_A1[Créer des comptes personnels]
        UC_A2[Gérer les comptes enseignants]
        UC_A3[Assigner des rôles et permissions]
        UC_A4[Configurer les paramètres académiques]
        UC_A5[Consulter les logs d'audit]
        UC_A6[Gérer les UE et Semestres]
        
        UC_A1 -.-> UC_A3 : include
        UC_A2 -.-> UC_A3 : include
    end

    Admin --- UC_A1
    Admin --- UC_A2
    Admin --- UC_A4
    Admin --- UC_A5
    Admin --- UC_A6
```
