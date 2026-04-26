# 🧠 Mémoire Technique & Contextuelle - Projet Bull ASUR (Ultra-Détaillé)

Ce document est la "boîte noire" du projet. Il consigne les décisions architecturales, l'état actuel des fonctionnalités et les règles de sécurité pour assurer une continuité parfaite entre les sessions de développement.

## 🏗️ 1. Architecture du Système & Stack

### Frontend (Nuxt 3)
- **Framework** : Nuxt 3 (SSR désactivé pour mode SPA backend-only).
- **Style** : Vanilla CSS 3 + Modern Aesthetics (Gradients, Glassmorphism, Micro-animations).
- **Navigation** : Système de **Sidebar Dynamique** centralisée dans `layouts/default.vue`. Les liens s'affichent selon le rôle Firebase/Supabase (`admin`, `secretariat`, `enseignant`, `etudiant`).
- **Dashboard Secrétariat** : Entièrement refait avec une approche analytique (cartes statistiques, flux d'activité, raccourcis métiers).

### Backend (Django 5 - DDD)
- **Structure** : Domain-Driven Design strict.
    - `domain/` : Logique métier pure (entités, services de calcul, interfaces).
    - `application/` : Cas d'utilisation (commandes, handlers, services d'application comme `AuditService`).
    - `infrastructure/` : Détails techniques (persistence Django ORM, Supabase Auth).
    - `interfaces/` : API REST via DRF (ViewSets, Serializers, Permissions).
- **Authentification** : Intégration Supabase via `request.auth` (Custom Middleware). Les claims Firebase sont portés dans le JWT.

## 🔐 2. Politique de Sécurité & RBAC (Robuste)

Nous avons implémenté un système de **filtrage par identité** (Strict Role-Based Access Control) sur tous les endpoints sensibles.

| Module | Règle de Visibilité (GET) | Règle d'Écriture (POST/PATCH/DEL) |
| :--- | :--- | :--- |
| **Étudiants** | Étudiant voit **uniquement lui-même**. Staff voit **Tout**. | Réservé au **Secrétariat / Admin**. |
| **Enseignants** | Enseignant voit **uniquement lui-même**. Staff voit **Tout**. | Réservé à l'**Admin**. |
| **Notes / Evals** | Étudiant voit ses notes. Enseignant voit ses matières. | Enseignant (Propriétaire) ou Admin. |
| **Absences** | Étudiant voit ses heures. Staff voit tout. | Réservé au **Secrétariat**. |
| **Résultats / PV** | Filtrage par `etudiant_id` ou `promo_id`. | Calcul automatique par le système. |
| **Référentiel** | Lecture Authentifiée. | Écriture réservée au **Secrétariat / Admin**. |

### Fichiers de Sécurité Clés :
- `backend/interfaces/api/permissions/role_permissions.py` : Définit `IsAdmin`, `IsSecretariat`, `IsEnseignant`, `IsEtudiant`.
- `backend/interfaces/api/views/` : Chaque ViewSet surcharge `get_permissions()` et la méthode `list()` / `retrieve()` pour appliquer le filtrage d'identité (via `request.user.username` qui est l'UID Firebase).

## 🧮 3. Moteur de Calcul Académique (DDD Core)

- **Calcul en Cascade (Atomicité)** :
    1. Saisie de Note -> `OrchestreCalcul` calcule `MoyenneMatiere`.
    2. `MoyenneMatiere` change -> Recalcul de la `MoyenneUE` (agrégation par coefficients).
    3. `MoyenneUE` change -> Recalcul de la `MoyenneSemestre`.
    4. Décision de Validation (Compensation : Moyenne >= 10 et aucune note < 07/20).
- **Rattrapage** : Si une note de type `RAT` est saisie, elle remplace la moyenne de la matière pour le calcul des UEs, mais la trace de l'échec initial est conservée.
- **Absences** : Chaque heure d'absence non justifiée peut impacter la moyenne finale via le service `CalculPénalité`.

## 🚩 4. État d'Avancement au 23 Avril 2026

### ✅ Terminé & Validé
- **Hub Secrétariat** : Interface complète (Étudiants, Absences, Enseignants, Délibérations, Référentiels, Bulletins).
- **Sécurisation Backend** : Audit de tous les viewsets terminé (aucun étudiant ne peut voir les données d'un autre).
- **Dashboard Analytique** : Statistiques en temps réel sur le dashboard du secrétariat.
- **Support Enseignants** : Saisie des notes restreinte aux matières assignées.
- **Logs d'Audit** : Traçabilité des modifications de notes via `AuditService`.

### 🛠️ 5. Correctifs de Stabilité et Sécurité (Session du 26/04/2026)

*   **Robustesse de l'Authentification (Supabase)** :
    *   **Problème** : Les erreurs 403 étaient causées par une validation de token locale (JWT decode) qui échouait si le `SUPABASE_JWT_SECRET` était mal configuré sur Render.
    *   **Solution** : Refactorisation de `SupabaseAuthentication` pour utiliser l'API officielle Supabase (`get_user`). Le backend valide désormais le token directement auprès de Supabase, éliminant toute dépendance aux clés secrètes locales pour la validation.
    *   **Compatibilité** : Ajout de l'attribut `uid` à l'objet `user` Django pour assurer la compatibilité avec toutes les commandes et handlers du backend.
*   **Correction des crashs 500 (Sérialisation)** :
    *   **Problème** : Crash lors de la récupération des listes d'enseignants ou de personnel car les entités DDD utilisaient des attributs privés (`_nom`, `_prenom`) sans propriétés publiques correspondantes, empêchant le sérialiseur DRF d'y accéder.
    *   **Solution** : Ajout des propriétés `@property` `nom` et `prenom` aux entités `Enseignant` et `Personnel`.
*   **Unification du RBAC** :
    *   Utilisation systématique de `request.user.role` injecté par le middleware d'auth.

### ⏳ 6. En cours / Priorités
- **Validation Finale (Prod)** : Vérifier que l'interface secrétariat charge désormais toutes les listes (Étudiants, Enseignants, Matières) sans erreur.
- **Génération PDF** : Finalisation du moteur Weasyprint pour les bulletins.
- **Verrouillage de session** : Implémenter le switch de verrouillage pour les délibérations.

## 📂 7. Cartographie des Fichiers Critiques
... (reste identique)

- **Permissions API** : `backend/interfaces/api/permissions/role_permissions.py`
- **Contrôle d'accès (Vues)** :
    - `backend/interfaces/api/views/etudiant_view.py`
    - `backend/interfaces/api/views/enseignant_view.py`
    - `backend/interfaces/api/views/evaluation_viewset.py`
    - `backend/interfaces/api/views/absence_viewset.py`
- **Orchestration Calcul** : `backend/domain/services/orchestre_calcul.py`
- **Logique UI Sidebar** : `frontend/layouts/default.vue`
- **Dashboard Secrétariat** : `frontend/pages/secretariat/index.vue`

## 💡 6. Directives pour les prochaines interventions
1. **Identité** : Toujours utiliser `request.user.username` pour récupérer l'UID Firebase de l'utilisateur actuel dans le backend.
2. **Design** : Les nouvelles interfaces doivent suivre le style "Rich Premium" (utiliser des gradients CSS et des composants d'UI haut de gamme).
3. **Tests** : Avant chaque push, vérifier que le rôle `etudiant` ne peut pas accéder aux stats de promotion (403 Forbidden).

---
*Ce fichier est mis à jour après chaque cycle majeur de développement.*
