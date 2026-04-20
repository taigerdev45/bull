from enum import Enum

class Mention(Enum):
    """Énumération des mentions académiques."""
    TRES_BIEN = "Très Bien"
    BIEN = "Bien"
    ASSEZ_BIEN = "Assez Bien"
    PASSABLE = "Passable"
    AJOURNE = "Ajourné"

    def __str__(self):
        return self.value
