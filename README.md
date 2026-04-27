#  Gestion des Bulletins de Notes - LP ASUR INPTIC

[![Django](https://img.shields.io/badge/Django-5.0-092E20?logo=django)](https://www.djangoproject.com/)
[![Nuxt.js](https://img.shields.io/badge/Nuxt.js-3-00DC82?logo=nuxt.js)](https://nuxt.com/)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?logo=supabase)](https://supabase.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> **Application de gestion des bulletins de notes pour la Licence Professionnelle Administration et Sécurité des Réseaux (LP ASUR) de l'Institut National de la Poste, des Technologies de l'Information et de la Communication (INPTIC).**

Automatisation complète du processus d'évaluation : saisie des notes, calculs pondérés, règles de compensation, décisions de jury et génération de bulletins PDF.

## 🛠️ Stack Technologique

- **Backend** : Django 5 (Django REST Framework) - Architecture DDD & SOLID.
- **Frontend** : Nuxt 3 (Vue.js), TailwindCSS.
- **Base de données** : PostgreSQL (via Supabase).
- **Authentification** : Supabase Auth (RBAC).
- **Déploiement** : Render (Backend), Vercel (Frontend).

## 📘 Documentation Technique

Toute la documentation technique est disponible dans le dossier `/docs` :

- **Architecture & Design** : [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Référentiel API** : [API.md](docs/API.md)
- **Règles Métier (Calculs)** : [REGLES_METIER.md](docs/REGLES_METIER.md)
- **Guide de Déploiement** : [DEPLOIEMENT.md](docs/DEPLOIEMENT.md)
- **Diagrammes UML (PlantUML)** : [UML/](docs/UML/)

---

## 📑 Table des matières

- [Contexte](docs/contexte.md)
- [Fonctionnalités](docs/features.md)
- [Architecture technique](docs/architecture.md)
- [Règles métier](docs/regles_metier.md)
- [Installation](docs/installation.md)
- [Utilisation](#-utilisation)
- [API Documentation](#-api-documentation)
- [Equipe](#-équipe)
- [Licence](#-licence)

---

## 🌍 Contexte
*Voir les détails dans [docs/contexte.md](docs/contexte.md).*

L'INPTIC assurait la formation LP ASUR avec un traitement manuel via Excel, entraînant des risques d'erreurs et un manque de traçabilité. Cette solution automatise l'ensemble de la chaîne de valeur pédagogique.

---

## ✨ Fonctionnalités
*Voir le détail des rôles et permissions dans [docs/features.md](docs/features.md).*

- **Gestion pédagogique** : Étudiants, UE, Matières.
- **Calculs automatiques** : Moyennes, Compensation, Crédits, Décisions de jury.
- **Édition des bulletins** : PDF conforme aux modèles officiels avec QR Code de vérification.
- **Sécurité & Droits** : RBAC (Admin, Secrétariat, Enseignant, Étudiant) via Supabase.

---

## 🏗️ Architecture technique
*Plus de détails techniques dans [docs/architecture.md](docs/architecture.md).*

Application moderne basée sur **Django 5** pour le backend et **Nuxt 3** pour le frontend. Respect strict des principes **SOLID** et du **Domain-Driven Design (DDD)** pour une maintenabilité optimale.

---

## 📏 Règles métier
*Référentiel complet dans [docs/regles_metier.md](docs/regles_metier.md).*

L'application intègre nativement le référentiel LP ASUR et les algorithmes de compensation spécifiques à l'INPTIC.

---

## ⚙️ Installation
*Guide complet disponible dans [docs/installation.md](docs/installation.md).*

1. Cloner le repository
2. Configurer Supabase (Database & Auth)
3. Initialiser le backend (venv, migrate, referentiel)
4. Lancer le frontend (npm install, npm run dev)
