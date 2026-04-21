# 🛠️ Guide d'Installation - Bull ASUR

Ce guide vous aide à installer le projet en local pour le développement.

## 1. Prérequis
- Python 3.12+
- Node.js 20+
- Compte **Supabase** (Gratuit)
- Git

## 2. Clonage et Configuration Backend
1. Clonez le dépôt : `git clone https://github.com/taigerdev45/bull.git`
2. Allez dans le dossier backend : `cd bull/bulletin-notes/backend`
3. Créez un environnement virtuel : `python -m venv venv` et activez-le.
4. Installez les dépendances : `pip install -r requirements.txt`
5. Configurez votre fichier `.env` (basé sur `.env.example`) avec vos credentials Supabase.

## 3. Initialisation de la Base de Données
```bash
# Appliquer les schémas
python manage.py migrate

# (Optionnel) Créer un administrateur initial
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
```

## 4. Configuration Frontend (Nuxt 3)
1. Allez dans le dossier frontend : `cd ../frontend`
2. Installez les modules : `npm install`
3. Configurez le `.env` avec l'URL de votre API locale (`http://localhost:8000`) et vos clés Supabase Client.
4. Lancez le client : `npm run dev`

---
## 5. Résolution des problèmes fréquents
- **Erreur de DB** : Vérifiez que votre `DATABASE_URL` utilise bien le mot de passe URL-encodé si vous avez des caractères spéciaux.
- **JWT Error** : Assurez-vous que le `SUPABASE_JWT_SECRET` dans votre `.env` backend correspond exactement à celui du dashboard Supabase.
