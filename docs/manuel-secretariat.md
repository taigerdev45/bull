# 📝 Manuel Secrétariat - Gestion des Notes et Étudiants

Le Secrétariat est le pilier opérationnel de l'application. Ce manuel vous guide à travers les processus de gestion académique.

## 1. Gestion des Étudiants

### Inscription d'un nouvel étudiant
1. Allez dans **Étudiants > Ajouter**.
2. Saisissez les données personnelles : Nom, Prénom, Email, Matricule, Date de Naissance, Bac, Provenance.
3. Le système crée automatiquement un compte de consultation pour l'étudiant.

### Mise à jour des dossiers
Vous pouvez éditer les informations à tout moment. Les changements sont réitérés instantanément sur le profil de l'étudiant.

## 2. Saisie des Notes (Évaluations)

Le système gère trois types d'évaluations : **CC (Contrôle Continu)**, **EXAMEN**, et **RATTRAPAGE**.

### Saisie manuelle
1. Sélectionnez une **Matière**.
2. Cliquez sur **Saisir les notes**.
3. Saisissez la note (de 0 à 20) pour chaque étudiant présent.
4. **Calcul Automatique** : Dès que vous enregistrez, le système recalcule automatiquement la moyenne de la matière, de l'UE et du semestre en cascade.

### Importation de masse (Excel)
Pour gagner du temps :
1. Téléchargez le **Modèle Excel** fourni dans l'interface d'import.
2. Remplissez les colonnes : Matricule, Code Matière, Type (CC/EXAM), Note.
3. Importez le fichier. Le système validera les données et vous affichera un rapport detaillé des succès et des erreurs.

## 3. Gestion des Absences

Chaque heure d'absence saisie sans justification peut entraîner un retrait automatique de points sur la moyenne de la matière concernée.
- Saisie via **Gestion des Absences**.
- Case à cocher **"Justifiée"** pour annuler la pénalité.

## 4. Résultats et Bulletins

### Délibération
Le système calcule la **Validation des UE** et les **Compensations** selon les règles métier (Section 4 du CDC). Vous pouvez consulter le statut de chaque étudiant (Admis, Redoublant, etc.).

### Édition des Bulletins
1. Accédez à **Résultats > Bulletins**.
2. Sélectionnez l'étudiant et le semestre (S5, S6 ou Annuel).
3. Cliquez sur **Générer PDF** pour obtenir un document officiel prêt à l'impression.

---
> [!TIP]
> Si une note de **Rattrapage** est saisie, elle remplace intégralement la moyenne initiale de la matière, quel que soit le score précédent.
