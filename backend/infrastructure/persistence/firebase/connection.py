import firebase_admin
from firebase_admin import credentials, firestore
import threading
from django.conf import settings

class FirebaseConnection:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(FirebaseConnection, cls).__new__(cls)
                cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialise la connexion Firebase de manière sécurisée."""
        if not firebase_admin._apps:
            import os
            import json
            
            # On tente de récupérer le JSON brut d'abord (recommandé pour Render/Vercel)
            raw_json = os.getenv('FIREBASE_SERVICE_ACCOUNT_JSON')
            cred_path = getattr(settings, 'FIREBASE_SERVICE_ACCOUNT_KEY', None)
            
            if raw_json:
                try:
                    cred_info = json.loads(raw_json)
                    cred = credentials.Certificate(cred_info)
                    firebase_admin.initialize_app(cred)
                except Exception as e:
                    print(f"Erreur lors du chargement du JSON Firebase: {e}")
                    # On tente de fallback sur le chemin de fichier
                    if cred_path:
                        cred = credentials.Certificate(cred_path)
                        firebase_admin.initialize_app(cred)
            elif cred_path:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
            else:
                # Fallback sur les credentials par défaut (utile pour GCP/ADC)
                firebase_admin.initialize_app()
                
        self.db = firestore.client()

    @property
    def client(self):
        return self.db
