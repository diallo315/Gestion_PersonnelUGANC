# Application/views.py
from django.shortcuts import render, redirect
from .models import *
import matplotlib.pyplot as plt
import io
import base64
from django.contrib.auth import authenticate, login, logout, get_user_model

import matplotlib
matplotlib.use('Agg')

#=========================================TABLEAU DE BORD =========================================#

def graphique_barresSexe():
    # Exemple de données (à remplacer par vos données réelles)
    labels = ['Homme', 'Femme']
    values = [60, 40]

    # Créer un graphe en barres
    plt.bar(labels, values)
    plt.xlabel('Sexe')
    plt.ylabel('Values')
    plt.title('Homme et Femme')
    plt.grid(True)

    # Convertir le graphique en image
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Convertir l'image en base64
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    return image_base64

def graphique_circulaireSexe():
    # Exemple de données (à remplacer par vos données réelles)
    labels = ['Homme', 'Femme']
    values = [60, 40]

    # Personnaliser le graphique circulaire
    colors = ['gold', 'lightcoral']

    # Création d'un graphique circulaire
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.title('Homme et Femme')

    # Convertir le graphique en image
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Convertir l'image en base64
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    return image_base64

def graphique_barresGrade():
    # Exemple de données (à remplacer par vos données réelles)
    labels = ['A1', 'A2','A3', 'B1', 'B2', 'C', 'CP']
    values = [10, 15, 15, 20, 15, 10, 15]

    # Créer un graphe en barres
    plt.bar(labels, values)
    plt.xlabel('Hiérarchie')
    plt.ylabel('Values')
    plt.title('Hiérarchie')
    plt.grid(True)

    # Convertir le graphique en image
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Convertir l'image en base64
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    return image_base64

def graphique_circulaireGrade():
    # Exemple de données (à remplacer par vos données réelles)
    labels = ['A1', 'A2','A3', 'B1', 'B2', 'C', 'CP']
    values = [10, 15, 15, 20, 15, 10, 15]

    # Personnaliser le graphique circulaire
    colors = ['#0f4c5c', '#e36414', '#fb8b24', '#c1121f', '#9a031e', '#5f0f40', '#eae2b7', '#fcbf49']

    # Création d'un graphique circulaire
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.title('Hiérarchie')

    # Convertir le graphique en image
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Convertir l'image en base64
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    return image_base64

def dashboard(request):
    # Appeler les fonctions de graphique
    graphique_barres_sexe = graphique_barresSexe()
    graphique_circulaire_sexe= graphique_circulaireSexe()
    graphique_barres_grade = graphique_barresGrade()
    graphique_circulaire_grade = graphique_circulaireGrade()
    
    context = {
        'graphique_barres_sexe': graphique_barres_sexe,
        'graphique_circulaire_sexe': graphique_circulaire_sexe,
        'graphique_barres_grade': graphique_barres_grade,
        'graphique_circulaire_grade': graphique_circulaire_grade
    }
    return render(request, 'src/dashboard.html', context)

#==========================CONNEXION ET INSCRIPTION ==============================#
def loginsignup(request):
    mot_de_pass_incoherent = ""
    Utilisateur_exist_deja = ""
    connexion_echouer = ""

    if request.method == "POST":
        try:
            is_connexion = request.POST.get("is_connexion")
            print(is_connexion)
            if is_connexion == 'on':
                emailrecu = request.POST.get("mail")
                password1 = request.POST.get("password1")
                user_connect = authenticate(request, username=emailrecu, password=password1)
                
                if user_connect:
                    print("j'ai authentifie " + emailrecu + " avec le mot de passe "+ password1)
                    login(request, user_connect)
                    return redirect('dashboard')
                else:
                    connexion_echouer = "La connexion a échoué. Veuillez vérifier vos informations d'identification."
            else:
                nom = request.POST.get("nom")
                prenom = request.POST.get("prenom")
                poste = request.POST.get("poste")
                mail = request.POST.get("mail")
                password1 = request.POST.get("password1")
                password2 = request.POST.get("password2")

                if password1 != password2:
                    mot_de_pass_incoherent = "Les mots de passe ne correspondent pas"
                else:
                    user_model = get_user_model()
                    instance, user_created = user_model.objects.get_or_create(
                        username=nom,
                        first_name=prenom,
                        last_name=nom,
                        email=mail,
                        poste=poste,
                    )

                    if user_created:
                        instance.set_password(password1)
                        instance.save()
                    else:
                        Utilisateur_exist_deja = "Cet utilisateur existe déjà"

        except Exception as e:
            print(f"Une erreur s'est produite : {e}")

    users = get_user_model().objects.all()
    context = {
        'utilisateurs': users,
        'Utilisateur_exist_deja': Utilisateur_exist_deja,
        'erreur_password': mot_de_pass_incoherent,
        'connexion_echouer': connexion_echouer,
    }

    return render(request, 'loginSignup.html', context)
#==================================PERSONNEL ============================================#
def personnel(request):
    personnel = Personnel.objects.all()
    administrationGeneral = AdministrationGeneral.objects.all()
    categorie = Categorie.objects.all()
    context = {
        'personnels' : personnel, 
        'administrationGenerals' : administrationGeneral,
        'categories': categorie,
    }
    return render(request, 'src/personnel.html', context)

#===============================AJOUT D'UN FONCTIONNAIRE===================================================#
def ajoutpersonnel(request):
    personnel_existant = ""
    personnel_enregistrer = ""
    if request.method == 'POST':
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        matricule = request.POST.get("matricule")
        hierarchie = request.POST.get("hierarchie")
        fonction = request.POST.get("fonction")
        grade = request.POST.get("grade")
        sexe = request.POST.get("sexe")
        diplome = request.POST.get("diplome")
        telephone = request.POST.get("tel")
        email = request.POST.get("email")
        dateNaissance = request.POST.get("dateN")
        lieuNaissance = request.POST.get("lieuN") 
        photo = request.POST.get("photo")
        salaire = request.POST.get("salaire")
        service = request.POST.get("service")
        observation = request.POST.get("observation")
        verifie_matricule = Personnel.objects.filter(matricule = matricule)
        if verifie_matricule.exists():
            personnel_existant = "Le personnel existe déjà !"
            print(personnel_existant)
            # return render(request, 'src/personnel.html', {'personnel_existe': personnel_existant})
        else:
            personnel = Personnel(
                nom = nom,
                prenom = prenom,
                matricule = matricule,
                sexe = sexe,
                hierarchie = hierarchie,
                fonction = fonction,
                grade = grade,
                diplome = diplome, 
                telephone = telephone,
                email = email,
                dateNaissance = dateNaissance,
                lieuNaissance = lieuNaissance,
                photo = photo,
                salaire = salaire,
                service = service,
                observation = observation
                
            )
            personnel.save()
            personnel_enregistrer = "Personnel enregistrer avec succès !"
            print(personnel_enregistrer)
            return redirect('personnel')
    context = {
        'personnel_enregistrer' : personnel_enregistrer,
        'personnel_existant' : personnel_existant,
    }
        
    return render(request, 'src/ajoutpersonnel.html', context)

#===============================DOCUMENT ===================================================#
def doucument(request):
    administrationGeneral = AdministrationGeneral.objects.all()
    context = {
        'administrationGenerals' : administrationGeneral,
    }
    return render(request, 'src/document.html', context)

def categorieag(request):
    return render(request, 'src/categorieAG.html')

#==========================================CONGE ======================================#
def conge(request):
    conge = Conge.objects.all()
    context = {
        'conges':conge,
    }
    return render(request, 'src/conge.html', context)

#==========================================AJOUT D'UN CONGE ======================================#
def ajoutconge(request):
    conges_existant = ""
    conges_success = ""
    
    if request.method == 'POST':
       matricule = request.POST.get("matricule")
       typeconge = request.POST.get("typeconge")
       dateD = request.POST.get("dateD")
       dateF = request.POST.get("dateF")
      
       try : 
            personnel = Personnel.objects.get(matricule = matricule) 
            conge = Conge(
                personnel = personnel,
                typeconge = typeconge,
                dateDeb = dateD,
                dateFin = dateF
            )
            conge.save()
            conges_success = "Congé enregistrer avec succcès ! On se retrouve le " + dateF + " "
            return render(request, 'src/conge.html', {'conges_success':conges_success})
       except:
           pass
       #verfie_matricule = Conge.objects.filter(personnel.matricule = matricu
       # le)
    #    conge = Conge(
    #        personnel.matricule = 
    #    )
    return render(request, 'src/ajoutconge.html')

#===================================INSCRIPTION A UNE FORMATION ===================================#
def inscritformation(request):
    return render(request, 'src/inscritformation.html')

#===================================HISTORIQUE ========================================================#
def historique(request):
    return render(request, 'src/historique.html')

#=========================================FORMATIONS EN COURS =========================================#
def formationcours(request):
    formation = Formation.objects.all()
    context = {
        'formations':formation,
    }
    return render(request, 'src/formationcours.html', context)

#=========================================FORMATIONS EN COURS =========================================#
def templates(request):
    messageDeconnexion = ""
    print("je suis la")
    if request.method == 'POST':
        deconnexion = request.POST.get('is_deconnect')
        print("JE SUIS DEDANS ET VOICI L'ETAT DE DECONNEXION " + deconnexion )
        if deconnexion == 'on':
            messageDeconnexion = "Merci d'avoir connsulter l'application "
            return render(request, 'src/loginSignup.html', {'messageDeconnexion': messageDeconnexion})
    return render(request, 'template.html')


