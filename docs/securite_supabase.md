# 🛡️ Sécurité & Authentification - Supabase

Ce document détaille l'architecture de sécurité mise en place pour l'application **Bull ASUR** après la migration vers Supabase.

## 1. Authentification (JWT)

L'authentification est gérée par **Supabase Auth (GoTrue)**. 

### Flux d'authentification
1. L'utilisateur se connecte via le Frontend (Nuxt 3).
2. Supabase retourne un **Access Token (JWT)**.
3. Ce token contient les métadonnées de l'utilisateur, notamment son **rôle** (`admin`, `secretariat`, `enseignant`, `etudiant`).
4. Toutes les requêtes vers le Backend Django incluent ce token dans le header `Authorization: Bearer <token>`.

## 2. Validation au Backend (Django)

Le middleware `SupabaseAuthentication` dans le backend assure une validation rigoureuse :
- **Validation Signature** : Utilisation du `SUPABASE_JWT_SECRET` pour garantir l'intégrité des jetons.
- **Authentification Résiliente** : Le système ne bloque pas les requêtes si le jeton est invalide tant que la vue cible est configurée en `AllowAny`. Cela évite les erreurs 403 inutiles sur les routes publiques.
- **Compatibilité Claims** : Pour assurer la compatibilité avec l'ancien code (Firebase), le middleware injecte automatiquement les claims dans `user.firebase_claims`.
- **Bypass Administrateur** : Sécurisation par email pour le compte propriétaire (`taigermboumba@gmail.com`) garantissant un accès super-utilisateur constant.

## 3. Row Level Security (RLS) - La Défense en Profondeur

En plus de la validation par l'API, la base de données PostgreSQL de Supabase applique des règles de sécurité au niveau des lignes (RLS). 

### Principes des Policies SQL
Même si un utilisateur parvient à contourner l'API, la base de données restreint l'accès :
- **is_admin** : Accès total à toutes les tables.
- **is_etudiant** : Ne peut lire que les lignes où `user_id = auth.uid()`.
- **is_enseignant** : Accès étendu aux évaluations mais restreint aux matières assignées.

## 4. Gestion des Rôles (RBAC)

Les rôles sont stockés dans les `user_metadata` du JWT pour une performance optimale (évite un appel DB à chaque requête).

| Rôle | Description |
| :--- | :--- |
| **admin** | Configuration système, gestion du personnel, audit logs. |
| **secretariat** | CRUD étudiants, saisie des notes, génération bulletins. |
| **enseignant** | Consultation listes, saisie des notes pour ses matières. |
| **etudiant** | Consultation de son profil et de ses propres résultats. |

---
> [!WARNING]
> Toute modification des rôles dans Supabase nécessite une reconnexion de l'utilisateur pour que le nouveau JWT soit généré avec les droits actualisés.
