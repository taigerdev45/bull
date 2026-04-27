from rest_framework import serializers

class NotificationSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    destinataire_uid = serializers.CharField(max_length=128)
    titre = serializers.CharField(max_length=200)
    message = serializers.CharField()
    is_read = serializers.BooleanField(default=False)
    type = serializers.CharField(max_length=50)
    created_at = serializers.DateTimeField(read_only=True)
