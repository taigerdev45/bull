from .event import Event

class EvaluationSupprimee(Event):
    """Émis lors de la suppression d'une note."""
    def __init__(self, data: dict, metadata: dict = None):
        super().__init__(data, metadata)
