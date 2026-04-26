from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from infrastructure.persistence.django_models.models import PersonnelModel

class ListPersonnelDebugView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        personnels = PersonnelModel.objects.all()
        return Response([
            {
                "email": p.email,
                "role": p.role,
                "user_id": p.user_id
            } for p in personnels
        ])
