# Fonctionnalités du Système Bull ASUR

## Gestion Académique
| Fonctionnalité | Description | État |
|:---|:---|:---|
| **Import / Export Excel** | Migration massive et extraction de données. | ✅ |
| **Profil Étudiant** | Vue 360° des notes, absences et progression ECTS. | ✅ |
| **Hub Secrétariat** | Console administrative Premium pour le pilotage global. | ✅ |
| **Gestion Personnel** | RBAC complet pour Admin, Secrétariat et Enseignants. | ✅ |
| **Référentiel ASUR**| Structure dynamique des UEs, Matières et Semestres. | ✅ |
| **Saisie en Temps Réel** | Calcul (DDD) immédiat des moyennes lors de la saisie. | ✅ |
| **Module Absences** | Décompte automatique et impact sur la validation. | ✅ |

## UX & Modernisation (v2.5)
- **Interface SaaS Premium** : Design monochrome professionnel, typographie moderne et glassmorphism.
- **Animation Cinétique** : Interaction "Antigravity Magnetic Ball" haute performance sur la page d'accueil.
- **Centre de Notifications** : Notification persistent avec nettoyage automatique (4 jours pour les lus).
- **Mode PWA** : Application installable sur PC, Android et iOS avec gestion de cache hors-ligne.
- **Suivi de Souris** : Effet de profondeur spatiale interactif.

## Génération de Documents (moteur jsPDF)
| Document | Format | Caractéristiques |
|:---|:---|:---|
| **Bulletin Semestriel** | PDF | Logo officiel, filigrane, tableau de notes, moyennes UE. |
| **PV de Délibération** | PDF | Récapitulatif anonymisé pour le jury de fin de cycle. |
| **Relevé Annuel** | PDF | Compilation des semestres S5 et S6. |

## Moteur de Calcul (DDD)
- **Logique Métier Complexe** : Moyennes pondérées, rattrapages (meilleure note gardée).
- **Système de Compensation** : Validation automatique par moyenne générale (seuil 10/20).
- **Gestion des Mentions** : Attribution dynamique (Passable, AB, Bien, TB).
- **Crédits ECTS** : Calcul automatique des 30/60 crédits par niveau.

## Sécurité & RBAC
- **Admin** : Maîtrise totale du socle technique et données.
- **Secrétariat** : Opérations administratives et éditions PDF.
- **Enseignant** : Saisie limitée à ses matières assignées.
- **Étudiant** : Accès restreint à ses propres informations.
