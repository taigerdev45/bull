# Fonctionnalités du Système

## Gestion des Étudiants

| Fonctionnalité | Description | État |
|:---|:---|:---|
| **Import Excel** | Ajout massif d'étudiants via fichier Excel. | ✅ |
| **Profil Étudiant** | Vue détaillée des notes et absences. | ✅ |
| **CRUD Étudiants** | Gestion des fiches administratives et suivis de parcours. | Admin, Secrétariat |
| **Référentiel LP ASUR** | Configuration des Coefficients et Crédits ECTS. | Admin |
| **Saisie des notes** | Entrée des notes CC, Examen et Rattrapage par matière. | Enseignant, Secrétariat |
| **Gestion des absences** | Suivi et pénalités automatiques sur la moyenne matière. | Secrétariat |

## Moteur de Calcul (DDD)

- **Moyenne matière** : Calcul pondéré ou remplacement par note de rattrapage.
- **Moyenne UE** : Agrégation intelligente avec coefficients.
- **Compensation** : Validation automatique des UEs par la moyenne générale du semestre (seuil 10.0).
- **Validation semestre** : Calcul des crédits ECTS acquis (cible 30 crédits).
- **Mentions** : Attribution automatique selon les paliers officiels (Passable, AB, Bien, TB).

## Bulletins & PV

| Type | Format | Description |
|:---|:---|:---|
| **Bulletin Semestriel** | PDF | Relevé de notes officiel du semestre. |
| **PV de Délibération** | PDF | Document récapitulatif pour le jury. |

## Gestion des Notes

* **Saisie Rapide** : Formulaire optimisé pour les enseignants.
* **Contrôle Continu** : Gestion de plusieurs devoirs par matière.
* **Examen Final** : Validation de la note d'examen (60%).

## Sécurité & Droits (RBAC)

| Rôle | Permissions |
|:---|:---|
| **Administrateur** | Accès total au référentiel et à la gestion des utilisateurs. |
| **Secrétariat** | Gestion quotidienne des notes, absences et génération des bulletins. |
| **Enseignant** | Saisie des notes restreinte à ses propres matières. |
| **Étudiant** | Consultation privée de ses propres relevés de notes. |
