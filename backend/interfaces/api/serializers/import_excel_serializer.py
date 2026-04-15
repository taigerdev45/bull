from rest_framework import serializers

class ImportExcelSerializer(serializers.Serializer):
    """Sérialiseur pour la validation de l'upload Excel."""
    fichier = serializers.FileField()
    promotion = serializers.CharField(required=False)
    annee = serializers.CharField(required=False)

    def validate_fichier(self, value):
        if not value.name.endswith('.xlsx'):
            raise serializers.ValidationError("Seuls les fichiers .xlsx sont acceptés.")
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Le fichier dépasse la taille maximale de 5MB.")
        return value
