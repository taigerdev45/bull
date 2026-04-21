from rest_framework import serializers

class EtudiantSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    matricule = serializers.CharField(max_length=50)
    date_naissance = serializers.DateField()
    lieu_naissance = serializers.CharField(max_length=200, required=False, allow_null=True)
    bac = serializers.CharField(max_length=100, required=False, allow_null=True)
    provenance = serializers.CharField(max_length=200, required=False, allow_null=True)


