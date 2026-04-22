# Guide de Test de l'API (Swagger UI)

Ce guide explique comment utiliser l'interface interactive Swagger pour tester les différents points d'entrée de l'API **Bulletin Notes**.

## 1. Accès à l'interface
L'interface Swagger est disponible à l'URL suivante (en local ou sur Render) :
`[BASE_URL]/api/schema/swagger-ui/`

Exemple local : `http://localhost:8000/api/schema/swagger-ui/`

## 2. Authentification (Étape Cruciale)
Toutes les routes (sauf l'authentification elle-même) nécessitent un token JWT.

### Récupérer un Token
1. Utilisez l'endpoint `/api/auth/login/` (si implémenté via une vue personnalisée) ou connectez-vous via l'application frontend.
2. Copiez le `access_token` reçu.

### Configurer Swagger
1. Sur la page Swagger UI, cliquez sur le bouton vert **Authorize** en haut à droite.
2. Dans le champ **Value**, collez votre token (ne pas ajouter le préfixe "Bearer", le système le gère automatiquement via la configuration `http bearer`).
3. Cliquez sur **Authorize** puis sur **Close**.

## 3. Structure des Tags
Les endpoints sont regroupés pour faciliter la navigation :
- **Authentification** : Gestion des accès et mot de passe.
- **Étudiants** : Gestion du cycle de vie des étudiants (Matricule, Inscription).
- **Évaluations** : Saisie des notes (individuelle ou en masse).
- **Absences** : Gestion des heures d'absence.
- **Académique** : Configuration des UE, Matières et Semestres.
- **Résultats** : Calcul des moyennes et génération des données de bulletins.
- **Administration** : Logs d'audit et paramètres système.

## 4. Astuces pour les Tests
- **Saisie Bulk** : Pour tester l'importation massive `/api/evaluations/bulk/`, envoyez une liste d'objets JSON.
- **Filtres** : Utilisez les paramètres de requête (query params) comme `?semestre=1` ou `?promotion=2024` directement dans les champs prévus par Swagger.
- **Codes de réponse** :
    - `200 OK` : Succès.
    - `201 Created` : Création réussie.
    - `401 Unauthorized` : Token manquant ou expiré.
    - `403 Forbidden` : Votre rôle (ex: Étudiant) n'autorise pas cette action.
    - `400 Bad Request` : Erreur de validation (vérifiez le format du JSON).

---
*Document généré par Antigravity pour faciliter le développement de Bulletin Notes.*
