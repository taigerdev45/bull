from rest_framework import serializers

class EvaluationSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    etudiant_id = serializers.CharField()
    matiere_id = serializers.CharField()
    enseignant_id = serializers.CharField(required=False, allow_null=True)
    type = serializers.ChoiceField(choices=['CC', 'EXAMEN', 'RATTRAPAGE'])
    note = serializers.FloatField(min_value=0, max_value=20)

    def validate_note(self, value):
        if not (0 <= value <= 20):
            raise serializers.ValidationError("La note doit être comprise entre 0 et 20.")
        return value
