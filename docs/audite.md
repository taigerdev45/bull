# Rapport d'Audit Technique - Système Bull ASUR

**Date :** 21 Avril 2026
**Auditeur :** Taiger Dev
**Statut Global :** En cours de développement (Nécessite des corrections structurelles critiques)

---

## 1. Analyse Backend (Architecture DDD & Firestore)

###  Points Forts

- **Respect du DDD :** Séparation claire entre `domain`, `application`, `infrastructure` et `interfaces`.
- **Injection de Dépendances :** Utilisation cohérente de `dependency-injector`.
- **Validation :** Les Value Objects (`Note`, `Moyenne`, `Coefficient`) valident correctement les invariants métier.

###  Points Résolus (Correctifs Appliqués)

1. **Normalisation du Schéma Firestore :**
   - **RÉSOLU :** Le champ `semestre_id` est désormais uniformisé sur des entiers (5, 6) dans tout le système (Initialisation, Repositories, Domain).
   - **RÉSOLU :** Le repository UE gère rétroactivement les anciens libellés ("Semestre 5") pour assurer la compatibilité.

2. **Implémentation de l'Orchestrateur :**
   - **RÉSOLU :** La méthode `recalculer_pour_etudiant` a été implémentée. Elle centralise le calcul en cascade et la persistance des résultats.

3. **Mismatches Typologiques & Bugs :**
   - **RÉSOLU :** L'orchestrateur et les calculateurs utilisent désormais des objets `Moyenne` consistants.
   - **RÉSOLU :** Correction du `TypeError` dans le calcul annuel (déballage des objets Moyenne).
   - **RÉSOLU :** Ajout du type `PONDEREE` dans l'Enum des moyennes.

### Problèmes Majeurs / Incohérences Logic

- **Moyenne Semestrielle :** RÉSOLU - Le calculateur ignore désormais les UEs vides (moyenne 0.0) lors du calcul de la moyenne générale, permettant un suivi précis en cours d'année.
- **Transactions Firestore :** Partiellement intégré dans les handlers. L'atomicité entre la note et le calcul est assurée au niveau du flux de commande.

---

## 2. Analyse Frontend (Nuxt 3 & Auth)

###  Points Forts

- **Aesthétique Premium :** UI très soignée, thèmes cohérents, micro-animations présentes.
- **Organisation :** Composables (`useApi`) et stores (Pinia) bien structurés.

###  Problèmes Critiques

1. **Authentification Simulée (Mock) :** Le fichier `login.vue` utilise toujours un `setTimeout` et ne contacte pas le backend. Le token Firebase n'est pas récupéré réellement.
2. **Gestion des Erreurs :** `useApi.ts` manque de gestion pour les codes d'erreur 401/403 (redirection vers login) et n'injecte pas dynamiquement le token JWT dans les headers.

---

## 3. Sécurité & Infrastructure

###  Sécurisation des Clés

- Les clés Firebase sont correctement ignorées par Git.
- Une procédure de déploiement via variables d'environnement (`FIREBASE_SERVICE_ACCOUNT_JSON`) a été ajoutée dans `docs/securite_firebase.md`.

###  Déploiement

- **Python 3.13 :** Le projet a été testé et corrigé pour être compatible (fix de `dependency-injector`).
- **Scripts CLI :** Les commandes de management Django sont maintenant intégrées à `manage.py`.

---

## 4. Résultats des Tests de Calcul (Audit Seeding)

Basé sur les simulations effectuées lors de cet audit :

- **Succès Direct :** ✅ (Après correction des types)
- **Compensation :** ✅ (Fonctionnelle si S5/S6 >= 10)
- **Rattrapage :** ✅ (Remplacement correct de la note d'examen)
- **Pénalité d'absence :** ✅ (Impacte correctement la moyenne de matière)

---

## 5. Recommandations Prioritaires (Plan d'Action)

1. **Refactorisation de l'Orchestrateur :** Implémenter `recalculer_pour_etudiant` et unifier les types de retour.
2. **Alignement du Schéma :** Normaliser les noms de champs (`semestre_id` partout) et les types (entiers vs chaînes).
3. **Connexion Auth :** Remplacer les mocks du frontend par les appels réels au backend Firebase.
4. **Implémentation PDF :** Intégrer une librairie de génération (ex: `borb` ou `WeasyPrint`) car le module est actuellement une coquille vide.

---

**Verdict :** L'application a une base architecturale très saine (DDD), mais l'implémentation actuelle souffre de "trous" fonctionnels et d'incohérences de nommage qui empêchent une utilisation en production. Le niveau d'avancement est de **65%**.
