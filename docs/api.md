# 📘 Documentation API Détaillée - Bulletin Notes (LP ASUR)

Cette documentation est destinée à l'équipe frontend pour faciliter l'intégration complète du système de gestion des notes de l'INPTIC.

---

## 🔐 1. Authentification & Sécurité

L'API utilise **Firebase Authentication** (JWT).

### Headers Standards
| Header | Valeur | Obligatoire | Description |
| :--- | :--- | :--- | :--- |
| `Authorization` | `Bearer <ID_TOKEN>` | Oui | Jeton d'identité Firebase (Firebase ID Token). |
| `Content-Type` | `application/json` | Oui | Pour toutes les requêtes avec corps (POST, PATCH, PUT). |

---

## 🎭 2. Rôles & Permissions

| Rôle | Portée des actions |
| :--- | :--- |
| `admin` | Accès total (Lecture/Écriture). |
| `secretariat` | Inscriptions, absences, configuration globale. |
| `enseignant` | Saisie et modification des notes pour ses matières. |
| `etudiant` | Lecture seule de ses propres données. |

---

## 📡 3. Référence des Endpoints

### 🎓 Étudiants (`/api/etudiants/`)
| Action | Méthode | URL |
| :--- | :--- | :--- |
| Lister | `GET` | `/api/etudiants/` |
| Consulter | `GET` | `/api/etudiants/{id}/` |

---

### 📝 Évaluations & Notes (`/api/evaluations/`)
| Action | Méthode | URL |
| :--- | :--- | :--- |
| Saisie | `POST` | `/api/evaluations/` |
| Bulk | `POST` | `/api/evaluations/bulk/` |
| Filtrer | `GET` | `/api/evaluations/?etudiant_id={id}` |

---

### 📊 Résultats Académiques (`/api/resultats/`)
#### Résultats Semestriels
- **URL** : `/api/resultats/semestre/{etudiant_id}/?semestre=5`
- **Méthode** : `GET`

**Structure de réponse type :**
```json
{
  "etudiant_id": "string",
  "semestre": 5,
  "moyenne_generale": 13.45,
  "credits_acquis": 30,
  "ues": [
    {
      "id": "UE5-1",
      "libelle": "Réseaux Pro",
      "moyenne_ue": 12.0,
      "statut": "VALIDÉ",
      "matieres": [
        {
          "libelle": "Cisco CCNA",
          "note_cc": 14.0,
          "note_examen": 10.0,
          "moyenne": 11.6
        }
      ]
    }
  ]
}
```

---

## 💻 4. Exemple d'Intégration (Nuxt 3/4)

### Composable `useApi` (composables/useApi.ts)
```typescript
export const useApi = () => {
  const authToken = useCookie('authToken')
  const baseUrl = 'https://api.lp-asur.ga'

  return {
    fetch: (url: string, options: any = {}) => {
      return $fetch(url, {
        baseURL: baseUrl,
        ...options,
        headers: {
          ...options.headers,
          Authorization: `Bearer ${authToken.value}`
        }
      })
    }
  }
}
```
