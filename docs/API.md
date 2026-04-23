# Documentation API - Bulletin de Notes

Toutes les requêtes API doivent être authentifiées via un Access Token (JWT) émis par Supabase. Base URL : `https://bull-api.onrender.com/api/`.

## Authentification
Format du header :  
`Authorization: Bearer <SUPABASE_ACCESS_TOKEN>`

---

## Liste des Endpoints Principaux

| Methode | Endpoint | Description | Roles Autorisés |
|---------|----------|-------------|-----------------|
| GET | /etudiants/ | Liste filtrée des étudiants. | Admin, Secrétariat (Tous), Étudiant (Soi-même) |
| POST | /etudiants/ | Inscription administrative. | Admin, Secrétariat |
| GET | /enseignants/ | Liste des enseignants. | Admin, Secrétariat (Tous), Enseignant (Soi-même) |
| GET | /absences/ | Liste des absences. | Admin, Secrétariat (Tous), Étudiant (Soi-même) |
| POST | /absences/ | Saisie d'une absence. | Admin, Secrétariat |
| GET | /ues/ | Référentiel des UEs. | Tous (Lecture), Secrétariat (Ecriture) |
| GET | /evaluations/ | Historique des notes. | Admin/Sec (Tous), Enseignant (Matières), Étudiant (Soi) |
| POST | /evaluations/ | Saisie d'une note. | Enseignant (Propriétaire), Admin |
| GET | /bulletins/donnees/{id}/ | Données bulletin. | Staff (Tous), Étudiant (Soi-même) |
| GET | /resultats/promotion/stats/ | Stats globales. | Admin, Secrétariat |

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
