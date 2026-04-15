# Guide de Deploiement - Bulletin de Notes

Ce document explique comment déployer l'application en production sur les plateformes Cloud recommandées.

## 1. Backend (Django + DRF) - Railway / Render

Le backend est conçu pour être déployé sur Railway.

### Etapes :
1. Connectez votre repository GitHub à Railway.
2. Ajoutez un service PostgreSQL (si migration SQL prévue) ou utilisez uniquement Firestore.
3. Configurez les variables d'environnement (voir section dédiée).
4. Le fichier Procfile ou le start command doit être :  
   gunicorn core.wsgi --log-file -

---

## 2. Frontend (React / Vue) - Vercel

Le frontend est optimisé pour Vercel.

### Etapes :
1. Créez un nouveau projet sur Vercel.
2. Liez votre branche main.
3. Définissez la commande de build : npm run build.
4. Répertoire de sortie : dist ou build.

---

## 3. Configuration Firebase (Infrastructure)

### Firestore :
- Créez un projet sur la console Firebase.
- Activez Firestore Database en mode production.
- Configurez les règles de sécurité (Audit et Auth).

### Authentification :
- Activez la méthode de connexion e-mail/mot de passe.
- Les utilisateurs (étudiants, enseignants) doivent être créés via la console ou via les API Admin.

---

## Variables d'Environnement (Secrets)

| Variable | Description | Exemple |
|----------|-------------|---------|
| FIREBASE_API_KEY | Clé API publique Firebase | AIzaSy... |
| FIREBASE_PROJECT_ID | ID du projet Firebase | bull-notes-asur |
| ADMIN_SDK_JSON | JSON du Service Account (Base64) | ewogICJ... |
| DATABASE_URL | Lien DB PostgreSQL (optionnel) | postgres://... |
| SECRET_KEY | Clé secrète Django | django-insecure-... |
| DEBUG | Mode debug (False en production) | False |
| ALLOWED_HOSTS | Domaines autorisés | api.lp-asur.ga, localhost |
