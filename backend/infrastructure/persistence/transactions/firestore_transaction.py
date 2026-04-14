from infrastructure.persistence.firebase.connection import FirebaseConnection

class FirestoreTransaction:
    """Utilitaire pour gérer les écritures groupées (Write Batch) dans Firestore."""

    def __init__(self, connection: FirebaseConnection):
        self.db = connection.client
        self._batch = None

    def __enter__(self):
        self._batch = self.db.batch()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._batch.commit()
        self._batch = None

    def set(self, doc_ref, data):
        self._batch.set(doc_ref, data)

    def update(self, doc_ref, data):
        self._batch.update(doc_ref, data)

    def delete(self, doc_ref):
        self._batch.delete(doc_ref)
