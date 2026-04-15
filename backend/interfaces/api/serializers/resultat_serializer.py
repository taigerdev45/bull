from rest_framework import serializers

class MatiereDetailSerializer(serializers.Serializer):
    id = serializers.CharField()
    libelle = serializers.CharField()
    coefficient = serializers.FloatField()
    note_cc = serializers.FloatField(required=False, allow_null=True)
    note_examen = serializers.FloatField(required=False, allow_null=True)
    note_rattrapage = serializers.FloatField(required=False, allow_null=True)
    moyenne = serializers.FloatField()
    penalite = serializers.FloatField()

class UEDetailSerializer(serializers.Serializer):
    id = serializers.CharField()
    code = serializers.CharField()
    libelle = serializers.CharField()
    moyenne_ue = serializers.FloatField()
    statut = serializers.CharField()
    credits_acquis = serializers.IntegerField()
    compensee = serializers.BooleanField()
    matieres = MatiereDetailSerializer(many=True)

class ResultatSemestreSerializer(serializers.Serializer):
    etudiant_id = serializers.CharField()
    semestre = serializers.IntegerField()
    moyenne_generale = serializers.FloatField()
    credits_acquis = serializers.IntegerField()
    total_credits = serializers.IntegerField()
    valide = serializers.BooleanField()
    ues = UEDetailSerializer(many=True)

class ResultatAnnuelSerializer(serializers.Serializer):
    etudiant_id = serializers.CharField()
    moyenne_annuelle = serializers.FloatField()
    total_credits = serializers.IntegerField()
    decision = serializers.CharField()
    mention = serializers.CharField()
    semestres = serializers.DictField(child=ResultatSemestreSerializer())

class BulletinSerializer(serializers.Serializer):
    etudiant = serializers.DictField() # Simplified for now
    type_bulletin = serializers.CharField()
    resultat_semestre = ResultatSemestreSerializer(required=False)
    resultat_annuel = ResultatAnnuelSerializer(required=False)
    date_generation = serializers.CharField()
    saisie_par = serializers.CharField()
