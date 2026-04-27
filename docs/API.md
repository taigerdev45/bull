# Documentation API - Bull ASUR

L'ensemble des services est accessible via `https://bull-api.onrender.com/api/`.

## Sécurité
L'authentification repose sur des jetons JWT valides.
- **Header** : `Authorization: Bearer <TOKEN>`
- **Cookie** : `auth_token` utilisé par le frontend Nuxt.

## Endpoints de Données
| Ressource | Méthode | Rôle requis | Action |
|:---|:---:|:---:|:---|
| `/etudiants/` | GET | Secretariat | Liste complète des étudiants. |
| `/etudiants/id/` | GET | Etudiant (Soi) | Détails du parcours universitaire. |
| `/evaluations/` | POST | Enseignant | Enregistrement d'une nouvelle note. |
| `/absences/` | POST | Secretariat | Déclaration d'une absence justifiée/injustifiée. |
| `/bulletins/pdf/{id}/`| GET | Staff | Téléchargement du relevé officiel. |

## Moteur de Calcul (DDD)
Les endpoints de résultats (`/resultats/`) déclenchent automatiquement l'orchestrateur de calcul qui applique :
1. Calcul des moyennes par matière (CC focus).
2. Agrégation des UEs avec coefficients.
3. Calcul de compensation semestrielle et annuelle.
4. Attribution des crédits ECTS et mentions.

## Notifications
Le système frontend synchronise les alertes académiques (nouvelles notes, retards, annonces) et gère leur persistance locale avec nettoyage automatique après 4 jours.
