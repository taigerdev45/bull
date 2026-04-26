from rest_framework import serializers

class EvaluationSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    etudiant_id = serializers.CharField()
    matiere_id = serializers.CharField()
    enseignant_id = serializers.CharField(required=False, allow_null=True)
    type = serializers.CharField() # On utilise CharField pour plus de souplesse à la lecture
    note = serializers.FloatField(min_value=0, max_value=20)
    date_evaluation = serializers.DateTimeField(source='date_saisie', read_only=True)
    matiere_libelle = serializers.CharField(read_only=True, required=False)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        
        # Récupération du libellé de la matière
        try:
            from infrastructure.config.dependency_injection import Container
            matiere_repo = Container.matiere_repo()
            matiere = matiere_repo.get_by_id(instance.matiere_id)
            if matiere:
                ret['matiere_libelle'] = matiere.libelle
            else:
                ret['matiere_libelle'] = "Matière Inconnue"
        except Exception:
            ret['matiere_libelle'] = "Matière Inconnue"

        # Gestion du type (Enum -> str)
        if hasattr(instance.type, 'name'):
            ret['type'] = instance.type.name
        
        # Gestion de la note (Note -> float)
        # On utilise déjà note_valeur dans l'entité, mais le sérialiseur cherche 'note'
        if hasattr(instance.note, 'valeur'):
            ret['note'] = instance.note.valeur
        elif isinstance(instance.note, (int, float)):
             ret['note'] = float(instance.note)
             
        return ret

    def validate_note(self, value):
        if not (0 <= value <= 20):
            raise serializers.ValidationError("La note doit être comprise entre 0 et 20.")
        return value
