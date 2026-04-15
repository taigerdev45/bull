from rest_framework import serializers
from datetime import date

class AbsenceSerializer(serializers.Serializer):
    """
    Sérialiseur pour les absences avec validation métier DRF.
    """
    id = serializers.CharField(read_only=True)
    etudiant_id = serializers.CharField(required=True)
    matiere_id = serializers.CharField(required=True)
    nombre_heures = serializers.IntegerField(required=True, min_value=0)
    date_absence = serializers.DateField(required=True)
    saisie_par = serializers.CharField(read_only=True)
    
    def validate_date_absence(self, value):
        if value > date.today():
            raise serializers.ValidationError("La date d'absence ne peut pas être dans le futur.")
        return value

    def validate_nombre_heures(self, value):
        if value <= 0:
            raise serializers.ValidationError("Le nombre d'heures doit être supérieur à zéro.")
        return value
