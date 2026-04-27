from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from interfaces.api.serializers.evaluation_serializer import EvaluationSerializer
from interfaces.api.permissions.role_permissions import IsAdmin, IsSecretariat, IsEnseignant, IsEtudiant
from interfaces.api.permissions.enseignant_matiere_permission import IsEnseignantMatiere
from application.commands.creer_evaluation_command import CreerEvaluationCommand
from application.commands.modifier_evaluation_command import ModifierEvaluationCommand
from application.commands.supprimer_evaluation_command import SupprimerEvaluationCommand
from application.handlers.evaluation_command_handler import EvaluationCommandHandler
from infrastructure.config.dependency_injection import Container

@extend_schema(tags=['Évaluations'])
class EvaluationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des évaluations.
    Supporte le CRUD, la saisie groupée (bulk) et le filtrage par rôle.
    """
    serializer_class = EvaluationSerializer
    
    def _get_handler(self) -> EvaluationCommandHandler:
        return Container.evaluation_command_handler()

    def _get_repo(self):
        return Container.evaluation_repo()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'bulk_creer']:
            return [IsEnseignantMatiere()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return []
            
        repo = self._get_repo()
        
        is_staff = getattr(user, 'is_staff', False)
        role = getattr(user, 'role', 'etudiant')
        
        if is_staff or role in ['admin', 'super_admin', 'secretariat']:
            return repo.obtenir_tout() if hasattr(repo, 'obtenir_tout') else []
            
        claims = getattr(user, 'firebase_claims', {})
        uid = user.username # UID stocké dans username
        
        if role == 'etudiant':
            return repo.obtenir_par_etudiant(uid)
        elif role == 'enseignant':
            matieres = claims.get('matieres', [])
            evals = []
            for m_id in matieres:
                evals.extend(repo.obtenir_par_matiere(m_id))
            return evals
        
        return []

    def perform_create(self, serializer):
        cmd = CreerEvaluationCommand(
            etudiant_id=self.request.data.get('etudiant_id'),
            matiere_id=self.request.data.get('matiere_id'),
            type_eval=self.request.data.get('type'),
            note=self.request.data.get('note'),
            saisie_par=self.request.user.uid
        )
        eval_id = self._get_handler().handle_creer(cmd)

    def perform_update(self, serializer):
        cmd = ModifierEvaluationCommand(
            evaluation_id=self.kwargs.get('pk'),
            nouvelle_note=self.request.data.get('note'),
            auteur=self.request.user.uid
        )
        self._get_handler().handle_modifier(cmd)

    def perform_destroy(self, instance):
        cmd = SupprimerEvaluationCommand(
            evaluation_id=self.kwargs.get('pk'),
            auteur=self.request.user.uid
        )
        self._get_handler().handle_supprimer(cmd)

    @extend_schema(
        summary="Saisie groupée de notes",
        description="Permet d'envoyer une liste d'évaluations en une seule requête.",
        request=EvaluationSerializer(many=True),
        responses={201: OpenApiTypes.OBJECT}
    )
    @action(detail=False, methods=['post'], url_path='bulk')
    def bulk_creer(self, request):
        """Action pour la saisie multiple de notes."""
        try:
            data = request.data
            evaluations_list = []
            
            # Support du format { evaluations: [...] } ou [...]
            if isinstance(data, dict) and 'evaluations' in data:
                evaluations_list = data['evaluations']
            elif isinstance(data, list):
                evaluations_list = data
            else:
                return Response({"error": "Format invalide. Liste ou objet {evaluations:[]} attendu."}, status=status.HTTP_400_BAD_REQUEST)
                
            commands = []
            for item in evaluations_list:
                # Validation minimale
                etudiant_id = item.get('etudiant_id')
                matiere_id = item.get('matiere_id') or data.get('matiere_id')
                type_eval = item.get('type')
                note_val = item.get('note')

                if not all([etudiant_id, matiere_id, type_eval]):
                    continue # Skip invalid entries

                cmd = CreerEvaluationCommand(
                    etudiant_id=etudiant_id,
                    matiere_id=matiere_id,
                    type_eval=type_eval,
                    note=note_val,
                    saisie_par=request.user.username
                )
                commands.append(cmd)
                
            if not commands:
                return Response({"error": "Aucune donnée valide à enregistrer."}, status=status.HTTP_400_BAD_REQUEST)

            self._get_handler().handle_bulk_creer(commands)
            return Response({"status": "Notes enregistrées avec succès"}, status=status.HTTP_201_CREATED)
            
        except KeyError as e:
            return Response({"error": f"Type d'évaluation invalide: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return Response({"error": f"Erreur serveur: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        summary="Lister les notes d'un étudiant",
        parameters=[OpenApiParameter("etudiant_id", OpenApiTypes.STR, OpenApiParameter.PATH)]
    )
    @action(detail=False, methods=['get'], url_path='etudiant/(?P<etudiant_id>[^/.]+)')
    def list_par_etudiant(self, request, etudiant_id=None):
        """Notes d'un étudiant spécifique."""
        role = getattr(request.user, 'role', 'etudiant')
        if role == 'etudiant' and request.user.username != etudiant_id:
            return Response({"error": "Accès refusé"}, status=status.HTTP_403_FORBIDDEN)
            
        evals = self._get_repo().obtenir_par_etudiant(etudiant_id)
        serializer = self.get_serializer(evals, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Lister les notes d'une matière",
        parameters=[OpenApiParameter("matiere_id", OpenApiTypes.STR, OpenApiParameter.PATH)]
    )
    @action(detail=False, methods=['get'], url_path='matiere/(?P<matiere_id>[^/.]+)')
    def list_par_matiere(self, request, matiere_id=None):
        """Notes d'une matière spécifique."""
        # Seule une personne autorisée peut lister par matière
        is_staff = getattr(request.user, 'is_staff', False)
        role = getattr(request.user, 'role', 'etudiant')
        
        if not is_staff and role == 'etudiant':
            return Response({"error": "Action réservée au staff"}, status=status.HTTP_403_FORBIDDEN)
            
        evals = self._get_repo().obtenir_par_matiere(matiere_id)
        serializer = self.get_serializer(evals, many=True)
        return Response(serializer.data)
