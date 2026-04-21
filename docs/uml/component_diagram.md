# Diagramme de Composants (Component Diagram)

Ce diagramme représente l'architecture logicielle de l'application "Bull ASUR" et les dépendances entre les modules.

```mermaid
componentDiagram
    package "Frontend (Nuxt 3)" {
        [Interface Utilisateur (UI)] as UI
        [Store / État Local] as Store
    }

    package "Backend (Django / DDD)" {
        [API REST (Controllers)] as API
        [Module Authentification (Supabase JWT)] as Auth
        [Module Gestion des Référentiels] as Ref
        [Module Calcul des Moyennes & Règles Métier] as Calc
        [Module Import/Export (Excel/JSON)] as IE
        [Module Génération des Bulletins (Logic)] as Bull
        [Couche d'Accès aux Données (ORM)] as ORM
    }

    database "Supabase" {
        [Base de Données PostgreSQL] as DB
        [Service d'Auth (GoTrue)] as SAuth
    }

    UI ..> API : Appel REST (HTTPS)
    API ..> Auth : Vérifie Identité
    Auth ..> SAuth : Valide JWT
    API ..> Ref : Orchestre
    Ref ..> Calc : Fournit Données
    Calc ..> ORM : Persiste
    IE ..> ORM : Lit/Écrit
    Bull ..> Calc : Utilise Résultats
    ORM ..> DB : SQL
```
