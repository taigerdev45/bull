# 🛠️ Manuel Administrateur - Bull ASUR (Supabase Edition)

Ce guide détaille les opérations critiques réservées aux administrateurs du système.

## 1. Gestion du Personnel et des Rôles

L'administrateur est le seul habilité à créer des comptes pour le Secrétariat et les autres Administrateurs.

### Création d'un compte personnel
1. Accédez au menu **Personnel** (icône 👥) dans la barre latérale.
2. Cliquez sur le bouton **➕ Nouveau Membre**.
3. Remplissez les champs nécessaires : Nom, Prénom, Email, Rôle et Téléphone.
4. Saisissez un **Mot de passe provisoire** (minimum 8 caractères). Ce mot de passe permettra à l'utilisateur de se connecter immédiatement.
5. Le système crée automatiquement l'utilisateur dans **Supabase Auth** et enregistre sa fiche dans le registre du personnel.

### Modification des permissions
Si vous changez le rôle d'un utilisateur, informez-le qu'il doit se **déconnecter et se reconnecter**. Son nouveau token (JWT) contiendra ses nouveaux privilèges.

## 2. Configuration du Référentiel Académique
Accédez au menu **Référentiels** (icône 📚) pour gérer la structure pédagogique.

### Unités d'Enseignement (UE)
- **Création** : Cliquez sur **➕ Créer une UE**. Le système créera automatiquement le semestre associé (S5, S6) s'il n'existe pas.
- **Code** : Utilisez un format standardisé (ex: `UE5-1`). C'est ce code qui sert de référence pour lier les matières.
- **Crédits** : Définissez le poids ECTS (généralement entre 2 et 8).

### Matières
- Chaque matière doit être rattachée à une UE.
- **Assignation Enseignant** : Depuis la liste des matières, vous pouvez assigner un enseignant responsable. Cet enseignant sera le seul (avec le staff) habilité à saisir les notes pour cette matière.
- **Coefficients** : Utilisés pour le calcul de la moyenne de l'UE.
- **Résilience** : Lors de la création d'une matière dans le portail admin, vous pouvez utiliser soit le **UUID interne** de l'UE, soit son **Code court**. Le système fera la correspondance automatiquement.

## 3. Paramètres Système & Seuils

Accédez à **Administration > Paramètres** pour configurer :
- **Paliers de mentions** : Définissez les seuils pour les mentions (Ex: 12 pour Assez Bien).
- **Pénalités d'absence** : Réglez la valeur de retrait par heure (par défaut -0.01 point).
- **Dates de clôture** : Activez ou désactivez la saisie des notes pour les enseignants.

## 4. Surveillance et Audit

Le module d'audit enregistre chaque action sensible de manière exhaustive :
- **Traçabilité complète** : Chaque log inclut l'action, l'utilisateur, l'adresse IP et l'agent utilisateur (navigateur).
- **Actions suivies** : Importations Excel, modifications de notes, attributions de matières, et suppressions.
- **Filtrage** : Utilisez les filtres par type d'entité ou par date pour retrouver une action spécifique.

Consultez les logs dans **Administration > Journaux d'Audit** pour garantir l'intégrité des résultats.

---
> [!CAUTION]
> Toute suppression d'une UE ou d'une Matière entraînera la suppression en cascade de toutes les notes associées. Préférez la désactivation si possible.
