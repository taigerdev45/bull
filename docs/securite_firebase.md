# Procédure de Sécurisation des Clés Firebase

Ce document détaille la procédure standard pour sécuriser les accès administratifs à Firebase dans l'environnement Bull ASUR.

## 1. Gestion du Fichier de Clé (Service Account)

> [!CAUTION]
> Ne jamais commiter le fichier `serviceAccountKey.json` ou toute clé privée dans le dépôt Git.

### Mesures en place :
- Le fichier `serviceAccountKey.json` est listé dans le `.gitignore`.
- En environnement local, chaque développeur possède sa propre clé fournie par l'administrateur Firebase.

## 2. Configuration en Production (Render / Heroku / CI/CD)

Pour la production, nous recommandons d'utiliser des **Variables d'Environnement** au lieu d'un fichier physique.

### Étapes recommandées :
1. **Conversion JSON en Base64 / String** :
   Copiez le contenu de votre JSON Firebase.
2. **Variable d'Environnement** :
   Créez une variable nommée `FIREBASE_SERVICE_ACCOUNT_JSON` sur votre plateforme de déploiement (ex: Render).
3. **Initialisation Dynamique (Python)** :
   Modifier `connection.py` pour détecter la variable d'environnement :

```python
import os
import json
import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    # Priorité 1 : Variable d'Environnement
    json_config = os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON')
    if json_config:
        cred_dict = json.loads(json_config)
        cred = credentials.Certificate(cred_dict)
    else:
        # Priorité 2 : Fichier local (développement)
        cred = credentials.Certificate('serviceAccountKey.json')
    
    firebase_admin.initialize_app(cred)
```

## 3. Contrôles d'Audit

- **Rotation des Clés** : Une rotation annuelle des clés privées est fortement conseillée.
- **Principe du Moindre Privilège** : Le compte de service utilisé par le Backend ne doit avoir que les rôles `Cloud Datastore User` et `Firebase Authentication Admin`.
