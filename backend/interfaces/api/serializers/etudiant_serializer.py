from rest_framework import serializers

class EtudiantSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    # password est optionnel : uniquement nécessaire si on crée un compte auth en même temps
    password = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)
    matricule = serializers.CharField(max_length=50)
    date_naissance = serializers.DateField()
    lieu_naissance = serializers.CharField(max_length=200, required=False, allow_null=True, allow_blank=True)
    bac = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    provenance = serializers.CharField(max_length=200, required=False, allow_null=True, allow_blank=True)
    status = serializers.CharField(max_length=50, required=False, allow_null=True, allow_blank=True, default='Inscrit')


