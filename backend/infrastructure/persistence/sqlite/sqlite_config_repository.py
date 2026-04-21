from typing import Dict, Any
from ..django_models.models import ParametreConfigModel
import json

class SQLiteConfigRepository:
    """Gère la configuration globale du système dans SQLite/Turso."""

    def get_settings(self) -> Dict[str, Any]:
        """Récupère les paramètres actuels depuis la DB ou les défauts."""
        settings = self._get_defaults()
        models = ParametreConfigModel.objects.all()
        for m in models:
            try:
                # On essaie de parser comme du JSON pour les listes
                settings[m.cle] = json.loads(m.valeur)
            except json.JSONDecodeError:
                # Sinon on garde la valeur string (ou on convertit en float/int si possible)
                val = m.valeur
                if val.lower() == 'true': val = True
                elif val.lower() == 'false': val = False
                else:
                    try:
                        if '.' in val: val = float(val)
                        else: val = int(val)
                    except ValueError:
                        pass
                settings[m.cle] = val
        return settings

    def update_settings(self, settings: Dict[str, Any]) -> None:
        """Met à jour les paramètres."""
        for key, value in settings.items():
            str_value = json.dumps(value) if isinstance(value, (list, dict)) else str(value)
            ParametreConfigModel.objects.update_or_create(
                cle=key,
                defaults={'valeur': str_value}
            )

    def _get_defaults(self) -> Dict[str, Any]:
        return {
            'reprise_soutenance_active': True,
            'reprise_soutenance_ues_exclues': ['UE6-2'],
            'penalite_absence_par_heure': 0.01,
            'seuil_validation_mention': [10.0, 12.0, 14.0, 16.0],
            'date_verrouillage_notes': None
        }
