# 📘 Documentation API Détaillée - Bulletin Notes (LP ASUR)

Cette documentation est destinée à l'équipe frontend pour faciliter l'intégration complète du système de gestion des notes de l'INPTIC.

---

## 🔐 1. Authentification & Sécurité

L'accès à l'API est protégé par Firebase Auth. Chaque requête doit inclure un jeton ID dans le header `Authorization`.

| Header | Valeur | Description |
| :--- | :--- | :--- |
| **Authorization** | `Bearer <TOKEN>` | Jeton obtenu via `firebase.auth().currentUser.getIdToken()` |
| **Content-Type** | `application/json` | Format de données requis pour toutes les requêtes POST/PATCH |

### Structure des Erreurs Auth

En cas d'échec d'authentification :

```json
{
  "detail": "Token Firebase invalide: [raison]",
  "code": "authentication_failed"
}
```

---

## 🎭 2. Rôles & Permissions

Les permissions sont basées sur les `Custom Claims` du token Firebase.

| Rôle | Portée des actions |
| :--- | :--- |
| `admin` | Accès total (Lecture/Écriture) sur toutes les ressources. |
| `secretariat` | Gestion des inscriptions, saisie des absences, configuration globale. |
| `enseignant` | Saisie et modification des notes pour les matières qui lui sont attribuées. |
| `etudiant` | Lecture seule de ses propres notes, absences et bulletins. |

---

## 📡 2. Endpoints Bulletins

### Données de Bulletin (`GET /api/bulletins/donnees/{etudiant_id}/`)

Recherche et gestion des apprenants.

| Action | Méthode | URL |
| :--- | :--- | :--- |
| Lister | `GET` | `/api/etudiants/` |
| Consulter | `GET` | `/api/etudiants/{id}/` |

**Réponse Type (Format JSON) :**

```json
[
  {
    "id": "etu-2024-001",
    "nom": "KOFFI",
    "prenom": "Jean",
    "matricule": "LPASUR001",
    "date_naissance": "2001-12-30"
  }
]
```

---

### 3. Endpoints Évaluations (Saisie de notes)

### Liste / Création (`GET` & `POST /api/evaluations/`)

Gestion des notes (CC, Examen, Rattrapage).

| Action | Méthode | URL | Description |
| :--- | :--- | :--- | :--- |
| Saisie | `POST` | `/api/evaluations/` | Création d'une note unique. |
| Bulk | `POST` | `/api/evaluations/bulk/` | Saisie massive pour une classe (Liste d'objets). |
| Filtrer | `GET` | `/api/evaluations/?etudiant_id={id}` | Liste des notes d'un étudiant. |

**Modèle de Saisie (POST) :**

```json
{
  "etudiant_id": "etu-123",
  "matiere_id": "mat-res-01",
  "type": "CC",
  "note": 15.25
}
```

---

### 📊 Résultats Académiques (`/api/resultats/`)

Calculs automatiques basés sur les règles de l'institut.

#### Résultats Semestriels
- **URL** : `/api/resultats/semestre/{etudiant_id}/?semestre=5`
- **Méthode** : `GET`

**Réponse Détaillée :**

```json
{
  "etudiant_id": "string",
  "semestre": 5,
  "moyenne_generale": 13.45,
  "credits_acquis": 30,
  "total_credits": 30,
  "valide": true,
  "ues": [
    {
      "id": "UE5-1",
      "libelle": "Réseaux Pro",
      "moyenne_ue": 12.0,
      "statut": "VALIDÉ",
      "credits_acquis": 6,
      "matieres": [
        {
          "libelle": "Cisco CCNA",
          "note_cc": 14.0,
          "note_examen": 10.0,
          "moyenne": 11.6,
          "penalite": 0.0
        }
      ]
    }
  ]
}
```

---

## 📏 4. Règles Métier (Business Rules)

Il est crucial que le frontend reflète ces règles pour la validation :

### Règles de Calcul

- **Pondération** : 40% CC / 60% Examen.
- **Rattrapage** : La note de rattrapage remplace la moyenne calculée si elle est supérieure.
- **Absences** : Une pénalité de -0.5 point par absence non justifiée est appliquée sur la moyenne de l'UE.
- **Compensation d'UE** : Une UE est validée si sa moyenne est ≥ 10/20. Une compensation peut s'appliquer selon le règlement.

---

## 💻 5. Exemple d'Intégration Avancée (Next.js)

### Exemple d'appel avec Axios

```javascript
import axios from 'axios';
import { getAuth } from 'firebase/auth';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

apiClient.interceptors.request.use(async (config) => {
  const auth = getAuth();
  const token = await auth.currentUser?.getIdToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Intercepteur pour gérer les erreurs globalement
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 403) {
      alert("Accès refusé : Vérifiez vos droits d'accès.");
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

---

## 📂 6. Imports/Exports & Audit

- **Import Excel** : `POST /api/import/evaluations/` (Corps : `multipart/form-data` avec champ `fichier`).
- **Export Excel** : `GET /api/export/resultats/?promotion=2024` (Retourne un flux binaire `.xlsx`).
- **Audit Logs** : `GET /api/audit/etudiant/{id}/` (Historique des modifications de notes pour la traçabilité).

---

## ❓ FAQ Intégration
- **Comment savoir si un étudiant a validé ?** Regardez le champ `valide: boolean` dans le résultat semestriel.
- **Les notes sont-elles en temps réel ?** Oui, chaque modification déclenche un recalcul via l'orchestrateur de domaine.
