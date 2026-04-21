from rest_framework import serializers
import re

class MatiereSerializer(serializers.Serializer):
    """Sérialiseur pour les matières."""
    id = serializers.CharField(read_only=True)
    libelle = serializers.CharField(max_length=200)
    coefficient = serializers.FloatField(min_value=1.0)
    credits = serializers.IntegerField(min_value=1)
    ue_id = serializers.CharField()
    enseignant_id = serializers.CharField(allow_null=True, required=False)

    def validate_libelle(self, value):
        if not value.strip():
            raise serializers.ValidationError("Le libellé ne peut pas être vide.")
        return value

class UESerializer(serializers.Serializer):
    """Sérialiseur pour les Unités d'Enseignement (UE)."""
    id = serializers.CharField(read_only=True)
    code = serializers.CharField(max_length=10)
    libelle = serializers.CharField(max_length=200)
    credits = serializers.IntegerField(min_value=1)
    semestre_id = serializers.CharField()
    matieres = MatiereSerializer(many=True, read_only=True)

    def validate_code(self, value):
        if not re.match(r'^UE[0-9]-[0-9]$', value):
            raise serializers.ValidationError("Le code UE doit être au format UE5-1, UE6-2, etc.")
        return value
