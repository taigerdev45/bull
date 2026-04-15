# Guide de Contribution

Merci de vouloir contribuer au projet **Bulletin de Notes - LP ASUR**. Voici les lignes directrices à suivre.

## 🤝 Standards de Code

- **PEP 8** : Le code Python doit respecter la norme PEP 8.
- **Type Hints** : Utilisez les annotations de type pour toutes les fonctions et méthodes.
- **Docstrings** : Utilisez le format Google pour la documentation des classes et fonctions.
- **Linters** : Avant de commit, lancez `black` et `flake8`.

## 🌳 Workflow Git

1. **Branche** : Créez une branche descriptive : `feature/nom-fonctionnalite` ou `fix/nom-bug`.
2. **Pull Request (PR)** : Ouvrez une PR vers `main`. Une PR doit être revue par au moins un autre membre de l'équipe.
3. **Draft** : Si votre travail n'est pas terminé, marquez la PR comme "Draft".

## 📝 Convention de Commit

Nous utilisons la convention **Angular/Conventional Commits** :

- `feat:` : Nouvelle fonctionnalité
- `fix:` : Correction de bug
- `docs:` : Modification de documentation
- `style:` : Changement de style (espace, formatage)
- `refactor:` : Modification du code sans changement de comportement
- `test:` : Ajout ou modification de tests
- `chore:` : Tâche de maintenance (ex: mise à jour Docker)

Exemple : `feat(api): ajouter endpoint de saisie par lot`

## ⚙️ Environnement de Developpement

1. Installez Docker et Docker Compose.
2. Lancez le projet : `docker-compose up`.
3. Accédez au backend sur `localhost:8000`.
