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

### 🛠️ 5. Correctifs de Stabilité et Synchronisation (Session du 26/04/2026)

*   **Unification de l'Extraction du Rôle (Sécurité)** :
    *   Correction du bug de priorité sur le rôle générique `'authenticated'` de Supabase.
    *   **Solution** : Utilisation systématique de `request.user.role` (injecté par `SupabaseAuthentication`) dans toutes les classes de permission (`IsSecretariat`, etc.) et ViewSets.
*   **Actualisation des Données Staff** :
    *   Restauration des variables d'état dans `etudiants.vue` et correction des endpoints API pour la saisie groupée des notes.
    *   Implémentation des méthodes `UPDATE` (PUT) et `PARTIAL_UPDATE` (PATCH) manquantes dans les ViewSets (`Personnel`, `Semestre`, `UE`, `Matière`, `Absence`).
*   **Résolution des Erreurs 403/405** : Les listes et modifications de données sont désormais 100% opérationnelles pour le personnel authentifié.

### ⏳ 6. En cours / Priorités
- **Génération PDF** : Finalisation du moteur Weasyprint pour l'édition de masse des bulletins PDF.
- **Workflow Délibération** : Validation finale du processus de "clôture de jury" (verrouillage des notes).
- **Vérification en Production** : Monitorer les logs Render pour confirmer la résolution définitive des 403.

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
