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
            
            # 1. On cherche la source (JSON brut ou chemin)
            # Priorité 1: Variable d'env directe
            # Priorité 2: Configuration settings (via FIREBASE_SERVICE_ACCOUNT_KEY_PATH)
            source = os.getenv('FIREBASE_SERVICE_ACCOUNT_JSON')
            if not source:
                source = getattr(settings, 'FIREBASE_SERVICE_ACCOUNT_KEY', None)
            
            if source:
                try:
                    # Est-ce du JSON brut ?
                    if isinstance(source, str) and source.strip().startswith('{'):
                        cred_info = json.loads(source)
                        cred = credentials.Certificate(cred_info)
                    else:
                        # C'est probablement un chemin de fichier
                        cred = credentials.Certificate(source)
                    
                    firebase_admin.initialize_app(cred)
                except Exception as e:
                    print(f"Tentative Firebase avec source brute échouée: {e}")
                    # Fallback sur ADC (GCP/Local auth)
                    try:
                        firebase_admin.initialize_app()
                    except Exception as e_adc:
                        print(f"Échec final de l'initialisation Firebase: {e_adc}")
            else:
                # Fallback par défaut
                firebase_admin.initialize_app()
                
        self.db = firestore.client()

    @property
    def client(self):
        return self.db
