#!/usr/bin/env bash
# exit on error
set -o errexit

# Naviguer vers le dossier backend
cd backend

# Installer les dépendances
pip install -r requirements.txt

# Collecter les fichiers statiques (pour Swagger)
python manage.py collectstatic --no-input

# Exécuter les migrations (nécessaire pour les sessions Django)
python manage.py migrate
