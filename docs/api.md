# Documentation API - Bulletin de Notes

Toutes les requêtes API doivent être authentifiées via un Token Firebase JWT. Base URL : https://api.lp-asur.ga/api/.

## Authentification
Format du header :  
Authorization: Bearer <FIREBASE_ID_TOKEN>

---

## Liste des Endpoints Principaux

| Methode | Endpoint | Description | Roles Autorises |
|---------|----------|-------------|-----------------|
| GET | /etudiants/ | Liste des étudiants. | Admin, Secrétariat |
| GET | /evaluations/ | Historique des notes (filtré par rôle). | Tous |
| POST | /evaluations/ | Saisie d'une nouvelle note. | Enseignant, Admin |
| POST | /evaluations/bulk/ | Saisie rapide par lot (liste d'objets). | Enseignant, Admin |
| GET | /resultats/semestre/{id}/ | Moyennes et crédits d'un semestre. | Tous (filtré) |
| GET | /bulletins/donnees/{id}/ | Données complètes pour génération PDF. | Étudiant, Admin |
| POST | /import/evaluations/ | Import via fichier Excel (.xlsx). | Secrétariat, Admin |
| GET | /audit/etudiant/{id}/ | Historique des modifications de notes. | Admin, Secrétariat |

---

## Exemples JSON

### 1. Saisie d'une Note (POST /api/evaluations/)

Requête :
```json
{
  "etudiant_id": "TEST2026001",
  "matiere_id": "MAT-001",
  "type": "CC",
  "note": 15.5
}
```

Réponse (201 Created) :
```json
{
  "id": "abc123xyz",
  "status": "Note enregistree avec succes"
}
```

### 2. Consultation Resultat (GET /api/resultats/semestre/S5/)

Réponse (200 OK) :
```json
{
  "etudiant_id": "TEST2026001",
  "moyenne_generale": 12.45,
  "credits_acquis": 30,
  "ues": [
    {
      "code": "UE5-1",
      "libelle": "Enseignement General",
      "moyenne_ue": 11.2,
      "statut": "ACQUISE_DIRECTE"
    }
  ]
}
```

---

## Codes Erreur

| Code | Signification | Cause Probable |
|------|---------------|----------------|
| 401 | Unauthorized | Token manquant ou expiré. |
| 403 | Forbidden | Rôle insuffisant ou matière non attribuée. |
| 400 | Bad Request | Données invalides (note > 20, format incorrect). |
| 404 | Not Found | Ressource inexistante (Étudiant, UE). |
| 409 | Conflict | Note déjà verrouillée par le jury. |
