from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
    poste = models.CharField(max_length=100)
    # Ajoutez ces lignes avec des noms personnalisés pour éviter le conflit
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to.",
        related_name="utilisateur_groups",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="utilisateur_user_permissions",
        related_query_name="user",
    )
    class Meta:
        db_table = 'T_Utilisateur'
        
class AdministrationGeneral(models.Model):
    nom = models.CharField(max_length = 100)
    def __str__(self):
        return f'{self.nom}'
    class Meta:
        db_table = 'T_AdministrationGeneral'
    

class Categorie(models.Model):
    administrationGeneral = models.ForeignKey(AdministrationGeneral, on_delete = models.CASCADE)
    nomcategorie = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.administrationGeneral.nom} {self.nomcategorie}'
    class Meta:
        db_table = 'T_Categorie'
    
class Statut(models.Model):
    nom = models.CharField(max_length = 50)
    def __str__(self) -> str:
        return f'{self.nom}'
    class Meta:
        db_table = 'T_Statut'

class Personnel(models.Model):
    matricule = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    hierarchie = models.CharField(max_length=50)
    sexe = models.CharField(max_length=50) 
    fonction = models.CharField(max_length=80)
    specialite = models.CharField(max_length=81)
    no_acte_affectation = models.CharField(max_length=50)
    grade = models.CharField(max_length=50)
    diplome = models.CharField(max_length=50)
    dateNaissance = models.DateField()
    date_enregistrement = models.DateField() 
    statut = models.ForeignKey(Statut, on_delete = models.CASCADE)
    categorie = models.ForeignKey(Categorie, on_delete = models.CASCADE)
    date_affectation = models.DateField()
    telephone = models.CharField(max_length=50)
    class Meta:
        db_table = 'T_Personnel'
   


class Document(models.Model):
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    nomDocument = models.CharField(max_length=30)
    typeDocument = models.CharField(max_length=30)
    dateEnregistrement = models.DateField()
    class Meta:
        db_table = 'T_Document'

class Conge(models.Model):
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    typeconges = models.CharField(max_length=50)
    dateDeb = models.DateField()
    dateFin = models.DateField()
    class Meta:
        db_table = 'T_Conge'

class RapportAnalytiques(models.Model):
    nom = models.CharField(max_length=50)
    class Meta:
        db_table = 'T_RapportAnalytiques'

class GenererRapport(models.Model):
    personnel = models.ForeignKey(Personnel, on_delete = models.CASCADE)
    rapportanalytique = models.ForeignKey(RapportAnalytiques, on_delete = models.CASCADE)
    class Meta:
        db_table = 'T_GenererRapport'

class Formation(models.Model):
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    programmeFormation = models.CharField(max_length=30)
    dateDeb = models.DateField()
    dateFin = models.DateField()
    class Meta:
        db_table = 'T_Formation'

class HFormation(models.Model):
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE)
    observation = models.CharField(max_length=50)
    class Meta:
        db_table = 'T_HFormation'