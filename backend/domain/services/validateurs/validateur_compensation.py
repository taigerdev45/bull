from typing import Dict
from domain.services.interfaces.i_validateur import IValidateur
from domain.value_objects.validation_result import ValidationResult, EtatAcquisition
from infrastructure.config.constants import SEUIL_REUSSITE

class ValidateurCompensation(IValidateur):
    """Logique critique de validation des UE et compensation par le semestre."""

    def valider(self, data: Dict) -> ValidationResult:
        """
        data: {
            'moyenne_ue': float,
            'moyenne_generale_semestre': float,
            'credits_ue': int
        }
        """
        moy_ue = data.get('moyenne_ue', 0.0)
        moy_gen = data.get('moyenne_generale_semestre', 0.0)
        credits = data.get('credits_ue', 0)

        # 1. Réussite directe
        if moy_ue >= SEUIL_REUSSITE:
            return ValidationResult(
                etat=EtatAcquisition.ACQUISE_DIRECTE,
                credits_acquis=credits,
                moyenne=moy_ue,
                message="UE acquise par réussite directe."
            )

        # 2. Compensation par la moyenne générale
        if moy_gen >= SEUIL_REUSSITE:
            return ValidationResult(
                etat=EtatAcquisition.COMPENSEE,
                credits_acquis=credits,
                moyenne=moy_ue,
                message=f"UE compensée par la moyenne semestrielle ({moy_gen:.2f})."
            )

        # 3. Échec
        return ValidationResult(
            etat=EtatAcquisition.NON_ACQUISE,
            credits_acquis=0,
            moyenne=moy_ue,
            message="UE non acquise."
        )
