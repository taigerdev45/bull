# 📘 Documentation API - Bulletin Notes (LP ASUR)

Ce document fournit les détails techniques nécessaires pour l'intégration du frontend Next.js avec le backend Django DDD.

---

## 🔐 Authentification & Headers

L'API est sécurisée via **Firebase Auth**. Chaque requête doit inclure le token d'identité dans les headers.

### Headers requis
| Header | Valeur | Description |
| :--- | :--- | :--- |
| `Authorization` | `Bearer <ID_TOKEN>` | Token récupéré via `auth.currentUser.getIdToken()`. |
| `Content-Type` | `application/json` | Format de données pour les requêtes `POST`, `PUT`, `PATCH`. |

### Rôles (Custom Claims)
Le backend vérifie les rôles suivants via le token :
- `admin` : Accès total.
- `secretariat` : Gestion des étudiants, absences et paramètres.
- `enseignant` : Saisie des notes pour ses matières uniquement.
- `etudiant` : Consultation de ses propres notes et bulletins.

---

## 📡 Endpoints de Ressources

### 🎓 Étudiants (`/api/etudiants/`)

| Action | Méthode | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| Lister | `GET` | `/api/etudiants/` | Récupère la liste de tous les étudiants. |
| Créer | `POST` | `/api/etudiants/` | Ajoute un nouvel étudiant. |
| Consulter | `GET` | `/api/etudiants/{id}/` | Détails d'un étudiant spécifique. |

**Exemple de Modèle (Étudiant) :**
```json
{
  "id": "uuid-string",
  "nom": "DOE",
  "prenom": "John",
  "matricule": "2024-INP-001",
  "date_naissance": "2002-05-15"
}
```

---

### 📝 Évaluations & Notes (`/api/evaluations/`)

| Action | Méthode | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| Saisie | `POST` | `/api/evaluations/` | Enregistre une note individuelle. |
| Saisie Groupée | `POST` | `/api/evaluations/bulk/` | Envoie une liste de notes pour une classe. |
| Modifier | `PATCH` | `/api/evaluations/{id}/` | Modifie une note existante. |
| Supprimer | `DELETE` | `/api/evaluations/{id}/` | Suppression (soft delete) d'une note. |

**Corps de requête (Saisie) :**
```json
{
  "etudiant_id": "etu-123",
  "matiere_id": "mat-maths",
  "type": "CC", // ou "EXAMEN", "RATTRAPAGE"
  "note": 14.5
}
```

---

### 📊 Résultats & Bulletins

| Action | Méthode | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| Résultat Semestre | `GET` | `/api/resultats/semestre/{etudiant_id}/?semestre=5` | Calcul temps réel du semestre. |
| Résultat Annuel | `GET` | `/api/resultats/annuel/{etudiant_id}/` | Moyenne annuelle et décision jury. |
| Données Bulletin | `GET` | `/api/bulletins/donnees/{etudiant_id}/?semestre=5` | Données formatées pour le PDF. |

---

### 🏫 Structure Académique

| Ressource | Méthode | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| UEs | `GET` | `/api/ues/` | Liste des Unités d'Enseignement. |
| Matières | `GET` | `/api/matieres/` | Liste des matières. |
| Par Enseignant | `GET` | `/api/matieres/enseignant/{id}/` | Matières attribuées à un prof. |

---

## 💻 Exemples d'Intégration (JavaScript/TypeScript)

### 🚀 Avec Axios
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

// Intercepteur pour ajouter le token Firebase automatiquement
api.interceptors.request.use(async (config) => {
  const user = firebase.auth().currentUser;
  if (user) {
    const token = await user.getIdToken();
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Exemple : Saisie d'une note
export const saveGrade = async (gradeData) => {
  try {
    const response = await api.post('/evaluations/', gradeData);
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la saisie :", error.response?.data);
    throw error;
  }
};
```

### 🌐 Avec Fetch API
```javascript
const getStudentResults = async (studentId, semester) => {
  const token = await firebase.auth().currentUser.getIdToken();
  
  const response = await fetch(`${API_URL}/resultats/semestre/${studentId}/?semestre=${semester}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });

  if (!response.ok) throw new Error('Erreur réseau');
  return await response.json();
};
```

---

## ⚠️ Codes d'Erreur Communs
- `401 Unauthorized` : Token manquant ou expiré.
- `403 Forbidden` : L'utilisateur n'a pas le rôle requis (ex: Étudiant tentant de saisir une note).
- `400 Bad Request` : Données invalides (ex: note > 20 ou format de date incorrect).
- `404 Not Found` : Étudiant ou matière inexistant.
