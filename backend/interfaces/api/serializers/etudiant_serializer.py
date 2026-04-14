from rest_framework import serializers

class EtudiantSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    matricule = serializers.CharField(max_length=50)
    date_naissance = serializers.DateField()

class EvaluationSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    etudiant_id = serializers.CharField()
    matiere_id = serializers.CharField()
    type = serializers.ChoiceField(choices=['CC', 'EXAMEN', 'RATTRAPAGE'])
    note = serializers.FloatField(min_value=0, max_value=20)

    def validate_note(self, value):
        if not (0 <= value <= 20):
            raise serializers.ValidationError("La note doit être comprise entre 0 et 20.")
        return value
