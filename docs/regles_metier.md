# ⚖️ Règles Métier & Algorithmes de Calcul

Ce document formalise les règles de calcul utilisées pour la délivrance des bulletins de notes de la LP ASUR.

## 1. Calcul de la Moyenne d'une Matière

Chaque matière est évaluée via un Contrôle Continu (CC) et un Examen.

**Formule Standard :**  
`Moyenne = (Note_CC * 0.4) + (Note_Examen * 0.6)`

**Cas Particuliers :**
- **Note Unique** : Si une seule note est saisie, elle compte pour 100% de la moyenne.
- **Rattrapage** : Si une note de rattrapage est saisie, elle **remplace intégralement** la moyenne calculée précédemment (Rattrapage = 100%).
- **Absences** : Chaque heure d'absence injustifiée entraîne une pénalité de **-0.01 pt** sur la moyenne de la matière concernée.

---

## 2. Calcul de la Moyenne d'une UE

L'Unité d'Enseignement (UE) agrège plusieurs matières pondérées par leur coefficient.

**Formule :**  
`Moyenne_UE = Σ(Moyenne_Matière_i * Coefficient_i) / Σ(Coefficients)`

---

## 3. Validation et Compensation

Le système suit les règles académiques de compensation annuelle.

### Acquisition d'une UE
- **Acquisition Directe** : `Moyenne_UE >= 10.0`. L'étudiant valide l'UE et obtient les crédits ECTS associés.
- **Compensation** : Si `Moyenne_UE < 10.0`, l'UE peut être compensée si la **Moyenne Générale du Semestre >= 10.0**. 
    - L'UE est alors marquée comme `COMPENSÉE`.
    - L'étudiant obtient tout de même les crédits ECTS.

### Validation du Semestre
Un semestre est validé si la moyenne pondérée de toutes les UEs du semestre est `>= 10.0`.

---

## 4. Mentions du Jury

Les mentions sont calculées sur la base de la Moyenne Générale Annuelle :

| Moyenne | Mention |
|---------|---------|
| [16, 20] | Très Bien |
| [14, 16[ | Bien |
| [12, 14[ | Assez Bien |
| [10, 12[ | Passable |
| < 10 | Ajourné (Échec) |
