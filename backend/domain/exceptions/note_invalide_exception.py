from .domain_exception import DomainException

class NoteInvalideException(DomainException):
    """Levée quand une note est en dehors des limites (0-20)."""
    pass
