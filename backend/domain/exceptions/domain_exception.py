class DomainException(Exception):
    """Classe de base pour les exceptions du domaine."""
    pass

class NoteInvalideException(DomainException):
    """Levée quand une note est en dehors des limites (0-20)."""
    pass

class CalculImpossibleException(DomainException):
    """Levée quand les données sont insuffisantes pour un calcul."""
    pass

class ValidationException(DomainException):
    """Levée lors d'une violation de règle métier."""
    pass
