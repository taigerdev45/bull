# 🧠 Mémoire Technique & Contextuelle - Projet Bull ASUR (Ultra-Détaillé)

Ce document est la "boîte noire" du projet. Il consigne les décisions architecturales, les évolutions majeures de l'UI et les règles métier pour assurer une continuité parfaite.

## 🏗️ 1. Architecture du Système & Stack (v2.5)

### Frontend (Nuxt 3 - Premium SaaS)
- **Design System** : Monochrome High-End. Utilisation de Vanilla CSS avec Glassmorphism et Gradients contextuels.
- **Micro-animations** :
    - **Page d'accueil** : Effet "Magnetic Bubble" cinétique sur canvas (80 particules orbitant le curseur).
    - **Transitions** : Navigation fluide via `fade-slide`.
- **Navigation** : Sidebar native (monochrome) avec icônes SVG épurées.
- **Notifications** : Système persistant avec nettoyage automatique des messages lus vieux de plus de **4 jours**.
- **Génération PDF** : Moteur client `jsPDF` + `jspdf-autotable` intégré dans `useExport.js` pour une édition instantanée des bulletins et PV.
- **PWA** : Support complet (installable sur PC/Mobile), icône native, cache Workbox et compatibilité iOS (black-translucent).

### Backend (Django 5 - DDD)
- **Structure** : Domain-Driven Design strict (Logique métier isolée des détails d'infrastructure).
- **Calcul DDD** : Orchestration temps réel des moyennes (Matière -> UE -> Semestre -> Crédits ECTS).
- **Authentification** : Validation sécurisée via Supabase Cloud API.
- **API** : RESTful avec filtrage strict par identité (RBAC).

## 🔐 2. Politique de Sécurité & RBAC
| Module | Visibilité | Écriture |
| :--- | :--- | :--- |
| **Profil Étudiant** | Privé (Possesseur) | Verrouillé (Système) |
| **Saisie Notes** | Enseignant (Ses matières) | Enseignant / Admin |
| **Bulletins** | Staff (Tous) | Secrétariat |
| **Référentiel** | Lecture Authentifiée | Admin / Secrétariat |

## 🚩 3. État d'Avancement au 27 Avril 2026

### ✅ Modernisation UI/UX Terminée (Wahou Effect)
- **Refonte Accueil** : Mise en place de l'effet magnétique haut de gamme, cartes SEO et optimisation mobile.
- **Harmonisation Dashboard** : Réduction des tailles de police (stats à 1.4rem-1.6rem) pour une sobrieté premium.
- **Export Bulletins** : PDF fonctionnel avec logo ministériel, filigranes et tableaux PDF ordonnés.
- **Notification Center** : Correction du bug de propagation de clic et automatisation du nettoyage.
- **PWA** : Correction du Manifest (start_url) et des icônes pour affichage sans arrière-plan système.

### 🛠️ Correctifs Majeurs de la Session
1. **Effet Bulle** : Transition d'une dispersion aléatoire vers une formation sphérique magnétique centrée sur la souris.
2. **Icons & Logos** : Restauration des couleurs d'origine et suppression des filtres CSS altérant les teintes.
3. **PWA** : Suppression du mode `maskable` pour éviter les bordures système sur l'icône de la barre des tâches.

## 📂 4. Cartographie des Fichiers Critiques
- **PWA Config** : `frontend/nuxt.config.ts`
- **Dashboard Admin** : `frontend/pages/admin/index.vue`
- **Dashboard Secrétariat** : `frontend/pages/secretariat/index.vue`
- **Dashboard Enseignant** : `frontend/pages/enseignant/index.vue`
- **Génération PDF** : `frontend/composables/useExport.js`
- **Animation Accueil** : `frontend/pages/index.vue` (Canvas Particle Engine)
- **Nettoyage Notifications** : `frontend/components/ui/NotificationCenter.vue`

## 💡 5. Directives pour les prochaines interventions
1. **Design** : Maintenir le style "Senior SaaS" (sobre, professionnel, monochrome). Pas de couleurs criardes.
2. **Composants** : Toujours vérifier la réactivité mobile des nouveaux tableaux et cartes statistiques.
3. **PWA** : Chaque mise à jour majeure doit être validée par une actualisation du Service Worker.

---
*Dernière mise à jour : 27/04/2026.*
