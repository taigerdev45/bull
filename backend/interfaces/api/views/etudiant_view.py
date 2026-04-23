from rest_framework import viewsets, status, views, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from interfaces.api.serializers.etudiant_serializer import EtudiantSerializer
from interfaces.api.serializers.evaluation_serializer import EvaluationSerializer
from interfaces.api.permissions.role_permissions import IsEnseignant, IsAdmin, IsSecretariat, IsEtudiant
from infrastructure.config.dependency_injection import Container


@extend_schema(tags=['Étudiants'])
class EtudiantViewSet(viewsets.ViewSet):
    """
    ViewSet CRUD étudiants.
    """
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsSecretariat()]
        return [permissions.IsAuthenticated()]

    # ─── LIST ────────────────────────────────────────────────────────────────
    def list(self, request):
        repo = Container.etudiant_repo()
        
        # Sécurité : un étudiant ne doit pas pouvoir lister tous les autres
        auth = request.auth if isinstance(request.auth, dict) else {}
        role = (auth.get('role') or getattr(request.user, 'role', 'etudiant')).lower()
        
        if role == 'etudiant':
            etudiants = [repo.get_by_id(request.user.username)]
            etudiants = [e for e in etudiants if e]
        else:
            etudiants = repo.list_all()
            
        serializer = EtudiantSerializer(etudiants, many=True)
        return Response(serializer.data)

    # ─── RETRIEVE ────────────────────────────────────────────────────────────
    def retrieve(self, request, pk=None):
        # Sécurité: un étudiant ne peut voir que son propre profil
        auth = request.auth if isinstance(request.auth, dict) else {}
        role = (auth.get('role') or getattr(request.user, 'role', 'etudiant')).lower()
        if role == 'etudiant' and request.user.username != pk:
            return Response({"error": "Accès refusé"}, status=status.HTTP_403_FORBIDDEN)

        repo = Container.etudiant_repo()
        etudiant = repo.get_by_id(pk)
        if not etudiant:
            return Response({'error': 'Étudiant introuvable.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EtudiantSerializer(etudiant)
        return Response(serializer.data)

    # ─── CREATE ──────────────────────────────────────────────────────────────
    def create(self, request):
        serializer = EtudiantSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        from domain.entities.etudiant import Etudiant

        data = serializer.validated_data
        password = data.get('password')
        user_id = None

        # Mode 1 : créer un compte Auth si un mot de passe est fourni
        if password:
            try:
                auth_service = Container.auth_service()
                display_name = f"{data['prenom']} {data['nom']}"
                user_id = auth_service.create_user(
                    email=data['email'],
                    password=password,
                    display_name=display_name
                )
                auth_service.set_user_claims(user_id, 'etudiant')
            except Exception as e:
                return Response(
                    {'error': f'Erreur de création du compte Auth : {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Mode 2 (et suite du mode 1) : enregistrement du dossier student
        try:
            repo = Container.etudiant_repo()
            etudiant = Etudiant(
                nom=data['nom'],
                prenom=data['prenom'],
                matricule=data['matricule'],
                email=data['email'],
                user_id=user_id,
                date_naissance=data['date_naissance'],
                lieu_naissance=data.get('lieu_naissance'),
                bac=data.get('bac'),
                provenance=data.get('provenance'),
            )
            repo.save(etudiant)
            # On retourne les données sans le mot de passe
            out = EtudiantSerializer(etudiant)
            return Response(out.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de la sauvegarde : {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    # ─── UPDATE (PATCH) ──────────────────────────────────────────────────────
    def partial_update(self, request, pk=None):
        repo = Container.etudiant_repo()
        etudiant = repo.get_by_id(pk)
        if not etudiant:
            return Response({'error': 'Étudiant introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        # On autorise les mises à jour partielles : tous les champs sont optionnels ici
        data = request.data
        if 'nom' in data:
            etudiant._nom = data['nom']
        if 'prenom' in data:
            etudiant._prenom = data['prenom']
        if 'matricule' in data:
            etudiant._matricule = data['matricule']
        if 'date_naissance' in data:
            etudiant._date_naissance = data['date_naissance']
        if 'lieu_naissance' in data:
            etudiant._lieu_naissance = data['lieu_naissance']
        if 'bac' in data:
            etudiant._bac = data['bac']
        if 'provenance' in data:
            etudiant._provenance = data['provenance']

        try:
            repo.save(etudiant)
            serializer = EtudiantSerializer(etudiant)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de la mise à jour : {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    # ─── UPDATE (PUT - fallback) ──────────────────────────────────────────────
    def update(self, request, pk=None):
        return self.partial_update(request, pk)

    # ─── DESTROY ─────────────────────────────────────────────────────────────
    def destroy(self, request, pk=None):
        repo = Container.etudiant_repo()
        try:
            repo.delete(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Évaluations'])
class EvaluationView(views.APIView):
    """Vue pour la saisie de notes déclenchant les commandes applicatives."""
    permission_classes = [IsEnseignant]

    def post(self, request):
        serializer = EvaluationSerializer(data=request.data)
        if serializer.is_valid():
            service = Container.evaluation_service()
            try:
                eval_id = service.saisir_note(
                    etudiant_id=serializer.validated_data['etudiant_id'],
                    matiere_id=serializer.validated_data['matiere_id'],
                    type_eval=serializer.validated_data['type'],
                    note=serializer.validated_data['note']
                )
                return Response({'id': eval_id, 'status': 'Calculé'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
