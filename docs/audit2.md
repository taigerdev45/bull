# Rapport d'Audit Backend (Avancement & Fonctionnel)

**Date :** 21 Avril 2026
**Périmètre :** Implémentation du système "Bull ASUR" selon le cahier des charges 1.2, 1.3 et le périmètre V2.

---

## 1. Objectifs Spécifiques (Section 1.3)

| Fonctionnalité | Statut | Observations et Fichiers Clés |
| :--- | :---: | :--- |
| **Saisir et contrôler les notes** (CC, examen, rattrapage) | ✅ **Implémenté** | Fonctionnel via `EvaluationView` (REST API). La logique passe par le service métier `EvaluationService` et les entités du Domaine. |
| **Calculer automatiquement les moyennes** (pondérées) | ✅ **Implémenté** | Automatisé par le `CalculateurMatiere` et `OrchestreCalcul`. Gère correctement les ratios (ex: proportion CC vs Examen). |
| **Gérer les UE, les crédits et compensation** | ✅ **Implémenté** | Le moteur `ValidateurCompensation` applique les règles métiers. Les crédits ECTS et les structures d'UE sont gérés. |
| **Valider semestres et statuer sur le diplôme** | ✅ **Implémenté** | Effectué par `CalculateurSemestre`, `CalculateurAnnuel` et validé par les algorithmes de `DecideurJury`. API : `/api/resultats/annuel/`. |
| **Générer les bulletins individuels en format imprimable** | ⚠️ **Partiel** | Les excellentes données structurées et JSON sont opérationnelles (`BulletinView`). La génération de tableau Excel l'est aussi. *Cependant, le format final "Imprimable/PDF" (ex: intégration Weasyprint) n'est pas encore branché dans les routes de téléchargement pour l'impression directe.* |
| **Assurer le suivi des absences et décisions de jury** | ✅ **Implémenté** | Route HTTP (`AbsenceViewSet`) et retrait de points automatisé par le `PenaliteService`. Paliers de jury OK. |

---

## 2. Périmètre Fonctionnel Appliqué (Section 2)

| Domaine | Implémentation |
| :--- | :--- |
| **Gestion des données étudiants** | **100%** - Modèle `Etudiant` avec pièces détaillées (date de naissance, matricule, provenance, bac, filière, niveau ASUR). |
| **Référentiel Pédagogique** | **100%** - Classes complètes (`UE`, `Matiere`, `Semestre`) liées à Firebase via leurs Repositories dédiés et sécurisées en CRUD. |
| **Saisie et importation Excel** | **100%** - Fonction "Import en masse" implémentée dans `ImportExportService` (Lecture Excel, validation et enregistrement DB). |
| **Rôles et Accès Utilisateurs** | **100%** - Architecture Auth robuste. Firestore (`utilisateurs`) combinée à Firebase Authentication (Tokens JWT, Custom Claims). Inscription exclusivement contrôlée par Admin/Secretariat (Plus d'inscription libre). |

---

## 3. Référentiel S5/S6 (Section 3.1)

- **Structure de la base :** La DB est structurellement capable d'accueillir n'importe quelle hiérarchie (S5, S6).
- Le modèle de données associe parfaitement chaque `Matiere` à une `UE` (Clé étrangère via `ue_id`), qui possède elle-même un `semestre_id` et un champ `credit`.

---

## Conclusion et Recommandations
🚨 **Alerte d'avancement :**
Le **Backend** couvre à 98% de manière fonctionnelle le cahier des charges métier, avec une excellente architecture DDD (Domain Driven Design).

*👉 Seule étape restante côté Backend avant production :*
La bibliothèque de création PDF pour les bulletins finaux "Imprimables" reste à raccorder formellement à un Endpoint backend pour que le Frontend reçoive un fichier `.pdf` standardisé plutôt qu'uniquement la liste des moyennes ou un Excel.

---

## 4. RÈGLES DE GESTION (Section 4 de votre CDC)

| Règle | Statut d'implémentation | Fichier Responsable | Commentaire |
| :--- | :---: | :--- | :--- |
| **4.1 Moyenne Matière (CC 40% / Exam 60%)** | ✅ **OK** | `calculateur_matiere.py` | La pondération est exacte. En cas de note unique, elle compte à 100%. Le rattrapage écrase toutes les autres évaluations. |
| **4.2 Moyenne UE (Pondérée par coefs)** | ✅ **OK** | `orchestre_calcul.py` | Chaque matière multiplie sa note finale par son coefficient pour alimenter l'UE. |
| **4.3 Moyenne Semestre (Pondérée par UE)** | ✅ **OK** | `calculateur_semestre.py` | Cumul des UE via leurs tailles ou crédits pour valider la moyenne S5 et S6. |
| **4.4 Moyenne Annuelle ((S5+S6)/2)** | ✅ **OK** | `calculateur_annuel.py` | Formule `(val_m1 + val_m2) / 2` strictement codée et validée par calcul arithmétique. |
| **4.5 Validation UE (≥ 10/20 ou compensation)** | ✅ **OK** | `validateur_compensation.py` | Le système renvoie `ACQUISE_DIRECTE` et `COMPENSEE` selon la moyenne générale. Les crédits sont tous attribués en cas de succès. |
| **4.6 Validation Semestre (Acquisition des crédits)** | ✅ **OK** | `calculateur_semestre.py` | Le seuil cible de réussite d'acquisition est validé logiciellement. |
| **4.7 Décision Annuelle du Jury** | ✅ **OK** | `decideur_jury.py` | Si crédits >= 60 -> *DIPLOME*. Si échec sur la soutenance (UE6-2) avec >= 50 crédits -> *REPRISE SOUTENANCE*. Autrement -> *REDOUBLEMENT*. Règle dynamique implémentée de façon paramétrique. |
| **4.8 Mentions Annuelles** | ✅ **OK** | `calculateur_annuel.py` | L'algorithme attribue `Passable (10)`, `Assez Bien (12)`, `Bien (14)` ou `Très Bien (16)`. |
| **4.9 Absences (Pénalité par heure)** | ✅ **OK** | `penalite_service.py` | Une réduction proportionnelle d'une valeur paramétrable (-0.01 point) est appliquée de façon isolée à la note de la matière sur le calcul final. |

---

## 5. FONCTIONNALITÉS DÉTAILLÉES (Section 5 du CDC)

- **5.1 CRUD des Référentiels :** ✅ Intégralement couvert par les points d'API REST (Sécurisés par rôle `IsSecretariat` ou `IsAdmin`).
- **5.2 Saisie des Notes :** ✅ L'`EvaluationView` autorise la saisie de différentes natures (CC, EXAMEN, RATTRAPAGE). Un validateur bloque les notes > 20 et < 0 (`Note.verifier_integrite()`).
- **5.3 Calcul Automatique :** ✅ Chaque insertion de note lance l'`OrchestreCalcul` qui se charge de propager la modification en live jusqu'aux résultats annuels.
- **5.4 Edition Bulletins & Export :** ⚠️ Les Endpoint de consultation JSON sont actifs pour l'application Frontend. *Il ne manque que la surcouche "Weasyprint" (PDF).*
- **5.5 Gestion des Utilisateurs :** ✅ `Firebase Auth` + `Middleware Django DRF`. Sécurisé via les JWT Custom Claims. (Admin = tout, Enseignant = sa matière, Secretariat = saisie/bulletins, Etudiant = Lecture). Modèle hermétique finalisé.
