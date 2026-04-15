#  Fonctionnalités Détaillées

##  Gestion pédagogique
| Fonctionnalité | Description | Rôle |
|----------------|-------------|------|
| **CRUD Étudiants** | Gestion des fiches administratives et suivis de parcours. | Admin, Secrétariat |
| **Référentiel LP ASUR** | Configuration des Coefficients et Crédits ECTS. | Admin |
| **Saisie des notes** | Entrée des notes CC, Examen et Rattrapage par matière. | Enseignant, Secrétariat |
| **Gestion des absences** | Suivi et pénalités automatiques sur la moyenne matière. | Secrétariat |

##  Moteur de Calcul (DDD)
- **Moyenne matière** : Calcul pondéré ou remplacement par note de rattrapage.
- **Moyenne UE** : Agrégation intelligente avec coefficients.
- **Compensation** : Validation automatique des UEs par la moyenne générale du semestre (seuil 10.0).
- **Validation semestre** : Calcul des crédits ECTS acquis (cible 30 crédits).
- **Mentions** : Attribution automatique selon les paliers officiels (Passable, AB, Bien, TB).

##  Sécurité & Droits (RBAC)
| Rôle | Permissions |
|------|-------------|
| **Administrateur** | Accès total au référentiel et à la gestion des utilisateurs. |
| **Secrétariat** | Gestion quotidienne des notes, absences et génération des bulletins. |
| **Enseignant** | Saisie des notes restreinte à ses propres matières. |
| **Étudiant** | Consultation privée de ses propres relevés de notes. |
