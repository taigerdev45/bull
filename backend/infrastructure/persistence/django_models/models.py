from django.db import models
import uuid

class BasePersistenceModel(models.Model):
    """Classe de base pour tous les modèles de persistance."""
    id = models.CharField(primary_key=True, max_length=100, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class SemestreModel(BasePersistenceModel):
    libelle = models.CharField(max_length=50) # ex: S5, S6
    
    def __str__(self):
        return self.libelle

class UEModel(BasePersistenceModel):
    code = models.CharField(max_length=50, unique=True)
    libelle = models.CharField(max_length=200)
    credits = models.IntegerField(default=0)
    semestre = models.ForeignKey(SemestreModel, on_delete=models.CASCADE, related_name='ues')
    
    def __str__(self):
        return f"{self.code} - {self.libelle}"

class EnseignantModel(BasePersistenceModel):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    matricule = models.CharField(max_length=50, unique=True)
    numero_telephone = models.CharField(max_length=20, null=True, blank=True)
    specialite = models.CharField(max_length=200, null=True, blank=True)
    user_id = models.CharField(max_length=128, unique=True, null=True, blank=True) # Supabase UID
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"

class MatiereModel(BasePersistenceModel):
    libelle = models.CharField(max_length=200)
    coefficient = models.FloatField(default=1.0)
    credits = models.IntegerField(default=0)
    ue = models.ForeignKey(UEModel, on_delete=models.CASCADE, related_name='matieres')
    enseignant = models.ForeignKey(EnseignantModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='matieres')
    
    def __str__(self):
        return self.libelle

class EtudiantModel(BasePersistenceModel):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    matricule = models.CharField(max_length=50, unique=True)
    user_id = models.CharField(max_length=128, unique=True, null=True, blank=True) # Supabase UID
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=200, null=True, blank=True)
    bac = models.CharField(max_length=100, null=True, blank=True)
    provenance = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.matricule})"

class EvaluationModel(BasePersistenceModel):
    TYPE_CHOICES = [
        ('CC', 'Contrôle Continu'),
        ('EXAMEN', 'Examen'),
        ('RATTRAPAGE', 'Rattrapage'),
    ]
    etudiant = models.ForeignKey(EtudiantModel, on_delete=models.CASCADE, related_name='evaluations')
    matiere = models.ForeignKey(MatiereModel, on_delete=models.CASCADE, related_name='evaluations')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    note = models.FloatField(null=True, blank=True)
    date_evaluation = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.etudiant} - {self.matiere} ({self.type})"

class AbsenceModel(BasePersistenceModel):
    etudiant = models.ForeignKey(EtudiantModel, on_delete=models.CASCADE, related_name='absences')
    matiere = models.ForeignKey(MatiereModel, on_delete=models.CASCADE, related_name='absences')
    heures = models.FloatField(default=0.0)
    date_absence = models.DateField()
    justifiee = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.etudiant} - {self.matiere} ({self.heures}h)"

class PersonnelModel(BasePersistenceModel):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('secretariat', 'Secrétariat'),
    ]
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    numero_telephone = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    user_id = models.CharField(max_length=128, unique=True) # Supabase UID
    derniere_connexion = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.role})"

class AuditLogModel(BasePersistenceModel):
    action = models.CharField(max_length=200)
    utilisateur_uid = models.CharField(max_length=128) # Firebase UID ou ID local
    details = models.TextField(null=True, blank=True)
    entity_id = models.CharField(max_length=100, null=True, blank=True)
    entity_type = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f"{self.action} par {self.utilisateur_uid}"

class ParametreConfigModel(BasePersistenceModel):
    cle = models.CharField(max_length=100, unique=True)
    valeur = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.cle}: {self.valeur}"

class ResultatUEModel(BasePersistenceModel):
    etudiant = models.ForeignKey(EtudiantModel, on_delete=models.CASCADE, related_name='resultats_ue')
    ue = models.ForeignKey(UEModel, on_delete=models.CASCADE, related_name='resultats')
    valeur_moyenne = models.FloatField()
    details = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.etudiant} - {self.ue} ({self.valeur_moyenne})"

class ResultatSemestreModel(BasePersistenceModel):
    etudiant = models.ForeignKey(EtudiantModel, on_delete=models.CASCADE, related_name='resultats_semestre')
    numero_semestre = models.IntegerField() # 1 à 8
    valeur_moyenne = models.FloatField()
    details = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.etudiant} - Semestre {self.numero_semestre} ({self.valeur_moyenne})"

class ResultatAnnuelModel(BasePersistenceModel):
    etudiant = models.ForeignKey(EtudiantModel, on_delete=models.CASCADE, related_name='resultats_annuels')
    annee_academique = models.CharField(max_length=20)
    valeur_moyenne = models.FloatField()
    details = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.etudiant} - {self.annee_academique} ({self.valeur_moyenne})"

class NotificationModel(BasePersistenceModel):
    destinataire_uid = models.CharField(max_length=128) # Supabase UID
    titre = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    type = models.CharField(max_length=50, default='INFO') # INFO, SUCCESS, WARNING

    def __str__(self):
        return f"[{'LU' if self.is_read else 'NON LU'}] {self.titre} pour {self.destinataire_uid}"
