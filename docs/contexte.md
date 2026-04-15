#  Contexte du Projet

## Le Problème
L'INPTIC (Institut National de la Poste, des TIC) assurait historiquement la formation LP ASUR (Licence Professionnelle Administration et Sécurité des Réseaux) avec un traitement manuel des notes. Cette méthode présentait plusieurs inconvénients majeurs :
- **Risques d'erreurs** : Les calculs de moyennes et de compensations via Excel étaient sujets à l'erreur humaine.
- **Manque de traçabilité** : Difficulté à suivre l'historique des modifications de notes.
- **Productivité réduite** : La préparation des sessions de jury et la génération des bulletins étaient chronophages.

## La Solution
Le projet "Bulletin de Notes LP ASUR" apporte une réponse automatisée et sécurisée à ces problématiques :
- **Calculs Certifiés** : Intégration rigoureuse des règles de pondération (40% CC, 60% Examen) et de compensation.
- **Traçabilité Totale** : Mise en place d'un audit log pour chaque action de modification.
-  **Génération Automatisée** : Création instantanée de bulletins PDF conformes aux modèles officiels.
-  **Centralisation** : Base de données Firestore centralisée et sécurisée par Firebase Auth.
