from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib.auth.admin import UserAdmin
@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
     list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'poste')

@admin.register(Statut)
class StatutAdmin(admin.ModelAdmin):
    list_display = ['nom']

@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ['matricule','nom', 'prenom', 'hierarchie', 
                    'sexe', 'fonction', 'specialite', 'no_acte_affectation',
                    'grade', 'diplome', 'dateNaissance', 'date_enregistrement', 
                    'statut', 'categorie', 'date_affectation', 'telephone']
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['personnel', 'nomDocument', 'typeDocument', 'dateEnregistrement']

@admin.register(Conge)
class CongeAdmin(admin.ModelAdmin):
    list_display = ['personnel', 'typeconges', 'dateDeb', 'dateFin']

@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display =['personnel', 'programmeFormation', 'dateDeb', 'dateFin']
    
@admin.register(HFormation)
class HFormationAdmin(admin.ModelAdmin):
    list_display =['formation','observation']
    
@admin.register(AdministrationGeneral)
class AdministrationGeneral(admin.ModelAdmin):
    list_display = ['nom']

@admin.register(Categorie)
class Categorie(admin.ModelAdmin):
    list_display = ['administrationGeneral', 'nomcategorie']

   
