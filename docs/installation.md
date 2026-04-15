#  Guide d'Installation

## Prérequis
- Python 3.12+
- Node.js 20+
- Compte Firebase (Spark ou Blaze)
- Git

## 1. Cloner le Projet
```bash
git clone https://github.com/taigerdev45/bull.git
cd bull/bulletin-notes
```

## 2. Configuration Firebase
1. Créer un projet sur [Firebase Console](https://console.firebase.google.com/).
2. Activer **Authentication** (Email/Password).
3. Activer **Firestore Database** en mode production.
4. Générer une nouvelle clé privée (Service Account) dans les paramètres du projet.
5. Renommer le fichier en `firebase-credentials.json` et le placer à la racine du dossier `backend/`.

## 3. Configuration Backend (Django)
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt

# Initialisation
python manage.py migrate
python manage.py initialiser_referentiel
python manage.py runserver
```

## 4. Configuration Frontend (Next.js)
```bash
cd ../frontend
npm install
npm run dev
```
