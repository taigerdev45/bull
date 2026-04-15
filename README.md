#  Gestion des Bulletins de Notes - LP ASUR INPTIC

[![Django](https://img.shields.io/badge/Django-5.0-092E20?logo=django)](https://www.djangoproject.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14-000000?logo=next.js)](https://nextjs.org/)
[![Firebase](https://img.shields.io/badge/Firebase-FFCA28?logo=firebase)](https://firebase.google.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> **Application de gestion des bulletins de notes pour la Licence Professionnelle Administration et Sécurité des Réseaux (LP ASUR) de l'Institut National de la Poste, des TIC (INPTIC).**

Automatisation complète du processus d'évaluation : saisie des notes, calculs pondérés, règles de compensation, décisions de jury et génération de bulletins PDF.

##  Documentation Technique

Toute la documentation technique est disponible dans le dossier `/docs` :

- **Architecture & Design** : [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Référentiel API** : [API.md](docs/API.md)
- **Règles Métier (Calculs)** : [REGLES_METIER.md](docs/REGLES_METIER.md)
- **Guide de Déploiement** : [DEPLOIEMENT.md](docs/DEPLOIEMENT.md)
- **Diagrammes UML (PlantUML)** : [UML/](docs/UML/)

---

##  Table des matières

- [Contexte](docs/contexte.md)
- [Fonctionnalités](docs/features.md)
- [Architecture technique](docs/architecture.md)
- [Règles métier](docs/regles_metier.md)
- [Installation](docs/installation.md)
- [Utilisation](#-utilisation)
- [API Documentation](#-api-documentation)
- [Screenshots](#-screenshots)
- [Équipe](#-équipe)
- [Licence](#-licence)

---

##  Contexte
*Voir les détails dans [docs/contexte.md](docs/contexte.md).*

L'INPTIC assurait la formation LP ASUR avec un traitement manuel via Excel, entraînant des risques d'erreurs et un manque de traçabilité. Cette solution automatise l'ensemble de la chaîne de valeur pédagogique.

---

##  Fonctionnalités
*Voir le détail des rôles et permissions dans [docs/features.md](docs/features.md).*

- **Gestion pédagogique** (Étudiants, UE, Matières)
- **Calculs automatiques** (Moyennes, Compensation, Crédits)
- **Édition des bulletins** (PDF conforme aux modèles officiels)
- **Sécurité & Droits** (RBAC via Firebase Auth)

---

##  Architecture technique
*Plus de détails techniques dans [docs/architecture.md](docs/architecture.md).*

Application moderne basée sur **Django 5 (DRF)** pour le backend et **Next.js 14** pour le frontend, utilisant **Firebase Firestore** comme base de données NoSQL. Respect strict des principes **SOLID** et du **Domain-Driven Design (DDD)**.

---

##  Règles métier
*Référentiel complet dans [docs/regles_metier.md](docs/regles_metier.md).*

L'application intègre nativement le référentiel LP ASUR et les algorithmes de compensation spécifiques à l'INPTIC.

---

##  Installation
*Guide complet disponible dans [docs/installation.md](docs/installation.md).*

1. Cloner le repository
2. Configurer Firebase
3. Initialiser le backend (venv, migrate, referentiel)
4. Lancer le frontend
