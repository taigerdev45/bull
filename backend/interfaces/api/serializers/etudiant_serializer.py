from rest_framework import serializers

class EtudiantSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    matricule = serializers.CharField(max_length=50)
    date_naissance = serializers.DateField()


