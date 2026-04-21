# 🛠️ Manuel Administrateur - Bull ASUR (Supabase Edition)

Ce guide détaille les opérations critiques réservées aux administrateurs du système.

## 1. Gestion du Personnel et des Rôles

L'administrateur est le seul habilité à créer des comptes pour le Secrétariat et les autres Administrateurs.

### Création d'un compte personnel
1. Accédez au menu **Administration > Équipe**.
2. Remplissez les informations (Nom, Prénom, Email).
3. **Sélection du Rôle** :
   - `admin` : Accès total à la configuration et aux logs d'audit.
   - `secretariat` : Accès à la gestion des étudiants et à la saisie des notes.
4. Le système crée l'utilisateur dans **Supabase Auth** et lui envoie un email de confirmation.

### Modification des permissions
Si vous changez le rôle d'un utilisateur, informez-le qu'il doit se **déconnecter et se reconnecter**. Son nouveau token (JWT) contiendra ses nouveaux privilèges.

## 2. Configuration du Référentiel Académique

Avant chaque semestre, l'administrateur doit vérifier la structure :
- **Semestres** : S5, S6 (ou plus si nécessaire).
- **UE (Unités d'Enseignement)** : Doivent avoir un code unique et un volume de crédits ECTS défini.
- **Matières** : Chaque matière doit être rattachée à une UE et posséder un coefficient de pondération.
- **Enseignants** : Liez chaque matière à son enseignant responsable pour lui donner l'accès à la saisie.

## 3. Paramètres Système & Seuils

Accédez à **Administration > Paramètres** pour configurer :
- **Paliers de mentions** : Définissez les seuils pour les mentions (Ex: 12 pour Assez Bien).
- **Pénalités d'absence** : Réglez la valeur de retrait par heure (par défaut -0.01 point).
- **Dates de clôture** : Activez ou désactivez la saisie des notes pour les enseignants.

## 4. Surveillance et Audit

Le module d'audit enregistre chaque action sensible :
- Qui a importé un fichier Excel ?
- Qui a modifié une note après sa saisie initiale (Horodatage + Utilisateur) ?
- Tentatives de connexions échouées.

Consultez les logs dans **Administration > Journaux d'Audit** pour garantir l'intégrité des résultats.

---
> [!CAUTION]
> Toute suppression d'une UE ou d'une Matière entraînera la suppression en cascade de toutes les notes associées. Préférez la désactivation si possible.
