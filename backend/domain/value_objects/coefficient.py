from dataclasses import dataclass

@dataclass(frozen=True)
class Coefficient:
    """Objet Valeur représentant un coefficient."""
    valeur: float

    def __post_init__(self):
        if self.valeur <= 0:
            raise ValueError("Le coefficient doit être strictement supérieur à 0.")

@dataclass(frozen=True)
class Credits:
    """Objet Valeur représentant les crédits ECTS."""
    valeur: int

    def __post_init__(self):
        if self.valeur < 0:
            raise ValueError("Les crédits ne peuvent pas être négatifs.")
