# Documentation UML - Système de Gestion des Bulletins

Ce répertoire contient l'intégralité des livrables UML requis pour la modélisation du système "Bull ASUR".

## 🗺️ 1. Diagrammes de Cas d'Utilisation (Vues Comportementales)
- [Vue Globale](uc_global.md) - Synthèse de tous les acteurs.
- [Rôle Administrateur](uc_admin.md) - Gestion technique et audit.
- [Rôle Secrétariat](uc_secretariat.md) - Gestion académique et saisies.
- [Rôle Enseignant](uc_enseignant.md) - Saisie des notes et listes.
- [Rôle Étudiant](uc_etudiant.md) - Consultation des résultats.

## 🏗️ 2. Diagrammes de Structure (Vues Statiques)
- [Diagramme de Classes](class_diagram.md) - Modèle de données et méthodes métier.
- [Diagramme de Composants](component_diagram.md) - Architecture logicielle modulaire.
- [Diagramme de Déploiement](deployment_diagram.md) - Architecture physique (Render/Supabase).

## 🔄 3. Diagrammes de Séquence (Vues Dynamiques)
- [Authentification](seq_auth.md) - Flux JWT Supabase.
- [Saisie Note & Recalcul](seq_note.md) - Cascade de calculs automatique.
- [Génération Bulletin](seq_bulletin.md) - Production du document PDF.
- [Import Excel](seq_import.md) - Traitement de masse des données.

## ⚙️ 4. Diagrammes d'Activité (Algorithmes)
- [Calcul des Moyennes](act_calcul.md) - Détail des pondérations et pénalités.
- [Validation UE](act_validation.md) - Règles de succès et compensation.
- [Décision du Jury](act_jury.md) - Logique de délibération annuelle.

## 🎢 5. Diagrammes d'États (Cycles de Vie)
- [Cycle de vie Étudiant](state_etudiant.md) - De l'inscription au diplôme.
- [Cycle de vie UE](state_ue.md) - États d'ouverture et de clôture.

---
*Note : Tous les diagrammes sont écrits en **Mermaid**. Ils peuvent être visualisés directement sur GitHub ou exportés via l'extension Mermaid de VS Code.*
