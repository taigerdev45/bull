from .event import Event

class EvaluationCreee(Event):
    """Émis lors de la création d'une note."""
    def __init__(self, data: dict, metadata: dict = None):
        super().__init__(data, metadata)