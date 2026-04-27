from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from dependency_injector.wiring import inject, Provide
from infrastructure.config.dependency_injection import Container
from rest_framework import serializers
from interfaces.api.permissions.role_permissions import IsAdmin, IsSecretariat

class EnseignantSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    matricule = serializers.CharField(max_length=50)
    telephone = serializers.CharField(max_length=20, required=False, allow_null=True, allow_blank=True)
    specialite = serializers.CharField(max_length=200, required=False, allow_null=True, allow_blank=True)
    password = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)
    matieres = serializers.ListField(child=serializers.CharField(), read_only=True)

@extend_schema(tags=['Administration'])
class EnseignantViewSet(viewsets.ViewSet):
    """ViewSet pour la gestion des Enseignants."""
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'assign_matieres']:
            return [IsSecretariat()]
        return [permissions.IsAuthenticated()]

    @inject
    def __init__(self, repo=Provide[Container.enseignant_repo], **kwargs):
        super().__init__(**kwargs)
        self.repo = repo

    def list(self, request):
        try:
            role = getattr(request.user, 'role', 'etudiant')
            is_staff = getattr(request.user, 'is_staff', False)
            
            if is_staff or role in ['admin', 'super_admin', 'secretariat']:
                enseignants = self.repo.list_all()
            elif role == 'enseignant':
                uid = getattr(request.user, 'uid', request.user.username)
                enseignants = [self.repo.get_by_user_id(uid)]
                enseignants = [e for e in enseignants if e]
            else:
                return Response({"error": "Acces restreint"}, status=status.HTTP_403_FORBIDDEN)
            
            # Enrichissement avec les matières (via Django ORM pour la performance)
            from infrastructure.persistence.django_models.models import MatiereModel
            matieres_dict = {} # e_id -> List[libelle]
            matieres_ids_dict = {} # e_id -> List[id]
            
            all_m = MatiereModel.objects.exclude(enseignant=None).select_related('enseignant')
            for m in all_m:
                e_id = m.enseignant.id
                if e_id not in matieres_dict:
                    matieres_dict[e_id] = []
                    matieres_ids_dict[e_id] = []
                matieres_dict[e_id].append(m.libelle)
                matieres_ids_dict[e_id].append(m.id)

            data = []
            for e in enseignants:
                s = EnseignantSerializer(e).data
                s['matieres'] = matieres_dict.get(e.id, [])
                s['matiere_ids'] = matieres_ids_dict.get(e.id, [])
                data.append(s)
                
            return Response(data)
        except Exception as e:
            import traceback
            return Response({
                "error": str(e),
                "traceback": traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        serializer = EnseignantSerializer(data=request.data)
        if serializer.is_valid():
            from domain.entities.enseignant import Enseignant
            
            data = serializer.validated_data
            email = data['email']
            password = data.get('password')
            matricule = data['matricule']
            auth_service = Container.auth_service()
            
            try:
                display_name = f"{data['prenom']} {data['nom']}"
                user_id = None
                
                # On tente d'abord de voir si l'utilisateur existe déjà pour éviter le crash 400
                existing_user = auth_service.get_user_by_email(email)
                if existing_user:
                    user_id = existing_user['uid']
                    print(f"[CREATION ENSEIGNANT] Utilisateur déjà existant: {email} -> {user_id}")
                elif password:
                    # Création seulement si mot de passe fourni et n'existe pas
                    user_id = auth_service.create_user(
                        email=email,
                        password=password,
                        display_name=display_name
                    )
                
                if user_id:
                    auth_service.set_user_claims(user_id, 'enseignant')
                
                enseignant = Enseignant(
                    nom=data['nom'],
                    prenom=data['prenom'],
                    email=email,
                    matricule=matricule,
                    telephone=data.get('telephone'),
                    specialite=data.get('specialite'),
                    user_id=user_id
                )
                
                enseignant.valider()
                self.repo.save(enseignant)
                
                return_data = serializer.data
                return_data.pop('password', None)
                return Response(return_data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                import traceback
                print(f"[ERROR CREATE ENSEIGNANT] {str(e)}\n{traceback.format_exc()}")
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            enseignant = self.repo.get_by_id(pk)
            if not enseignant:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            # Enrichissement avec les matières
            from infrastructure.persistence.django_models.models import MatiereModel
            matieres = MatiereModel.objects.filter(enseignant_id=pk)
            
            data = EnseignantSerializer(enseignant).data
            data['matieres'] = [m.libelle for m in matieres]
            data['matiere_ids'] = [m.id for m in matieres]
            
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        enseignant = self.repo.get_by_id(pk)
        if not enseignant:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = EnseignantSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            enseignant._nom = data['nom']
            enseignant._prenom = data['prenom']
            enseignant._email = data['email']
            enseignant._matricule = data['matricule']
            enseignant._telephone = data.get('telephone')
            enseignant._specialite = data.get('specialite')
            self.repo.save(enseignant)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        enseignant = self.repo.get_by_id(pk)
        if not enseignant:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        for key, value in request.data.items():
            if hasattr(enseignant, f"_{key}"):
                setattr(enseignant, f"_{key}", value)
        
        self.repo.save(enseignant)
        return Response(EnseignantSerializer(enseignant).data)

    @action(detail=True, methods=['post'], url_path='assign-matieres')
    def assign_matieres(self, request, pk=None):
        """Assigne plusieurs matières à un enseignant."""
        matiere_ids = request.data.get('matiere_ids', [])
        if not isinstance(matiere_ids, list):
            return Response({"error": "liste attendue"}, status=status.HTTP_400_BAD_REQUEST)
        
        matiere_repo = Container.matiere_repo()
        notification_repo = Container.notification_repo()
        
        assigned_names = []
        for m_id in matiere_ids:
            matiere = matiere_repo.get_by_id(m_id)
            if matiere:
                matiere_repo.attribuer_enseignant(m_id, pk)
                assigned_names.append(matiere.libelle)
        
        if assigned_names and pk:
            # Récupérer le user_id de l'enseignant pour la notification
            enseignant = self.repo.get_by_id(pk)
            if enseignant and enseignant.user_id:
                from domain.entities.notification import Notification
                notif = Notification(
                    destinataire_uid=enseignant.user_id,
                    titre="Nouvelles matières assignées",
                    message=f"Vous avez été assigné aux matières suivantes : {', '.join(assigned_names)}",
                    type="SUCCESS"
                )
                notification_repo.save(notif)
            
        return Response({"status": "matières assignées"})

    def destroy(self, request, pk=None):
        self.repo.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
