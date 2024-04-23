# Application/views.py
from django.shortcuts import render,get_object_or_404, redirect
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

#==================================DETAILS D'UN PERSONNEL ============================================#
def detailspersonnel(request, id):
    personnel = Personnel.objects.get(id = id)
    context = {
        'personnel' : personnel, 
    }
    return render(request, 'src/detailspersonnel.html', context)


#===============================DOCUMENT ===================================================#
def doucument(request):
    administrationGeneral = AdministrationGeneral.objects.all()
    context = {
        'administrationGenerals' : administrationGeneral,
    }
    return render(request, 'src/document.html', context)

#===============================TYPE DE DOCUMENT ===================================================#
def typedocument(request, id):
    typedocument = TypeDocument.objects.all()
    categorie = Categorie.objects.get(id = id)
    context = {
        'typedocuments' : typedocument,
        'categorie' : categorie,
    }
    return render(request, 'src/typedocument.html', context)

#===============================DOCUMENT ===================================================#
def ajoutdocument(request, id):
    matricule_exist =""
    accept = ""
    typedocument = TypeDocument.objects.get(id=id)
    if request.method == "POST":
        mat = request.POST.get("matricule")
        nomdoc = request.POST.get("nomdoc")
        doc = request.POST.get("doc")
        is_accept = request.POST.get("is_accept")
        personnel = Personnel.objects.get(matricule = mat)
        if is_accept:
            if personnel:
                document = Document(
                    personnel = personnel,
                    nomdocument = nomdoc,
                    typeDocument = typedocument,
                    document = doc,
                    date = timezone.now
                )
                document.save()
                message_success = "Enrgistré avec succès"
                return render(request, 'src/documentCAT.html', {'message_succes': message_success})
            else:
                matricule_exist = "Cette personne n'existe dans votre Base donnée"
        else:
            accept = "Confirmé l'ajout du Document"
    context = {
        'typedocument' : typedocument,
        'matricule_exist':matricule_exist,
        'accept': accept,
    }
    return render(request, 'src/ajoutdocument.html', context)

#===============================DOCUMENT ADMINISTRATIF GENERAL ===================================================#
def categorieag(request, id):
    administrationgeneral = AdministrationGeneral.objects.get(id = id)
    categorie = Categorie.objects.filter(administrationGeneral = administrationgeneral)
    context = {
        'categories' : categorie,
        'administrationgeneral' : administrationgeneral,
    }
    return render(request, 'src/categorieAG.html', context)

#===============================DOCUMENT CATEGORIE ===================================================#
def documentCAT(request, id):
    categorie = Categorie.objects.get(id = id)
    personnel = Personnel.objects.filter(categorie = categorie)
    document = Document.objects.filter(personnel__in = personnel)
    context = {
        'personnels' : personnel,
        'categorie':categorie,
        'documents' : document,
    }    
    return render(request, 'src/documentCAT.html', context)

#===============================DOCUMENT GENERE ===================================================#
def genereDocL(request, id):
    tlettre = TypeLettre.objects.get(id=id)
    context = {
        'tlettre' : tlettre,
    }
    return render(request, 'src/genereDocL.html', context)

#===============================DOCUMENT GENERE ===================================================#
def genereDocB(request, id):
    tbanque = TypeBanque.objects.get(id = id)
    context = {
        'tbanque':tbanque,
    }
    return render(request, 'src/genereDocB.html', context)

#===================================DOCUMENT ANALYTIQUE===================================#
def documentanalytique(request):
    tlettre = TypeLettre.objects.all()
    tbanque = TypeBanque.objects.all()
    context = {
        'tlettres':tlettre,
        'tbanques':tbanque,
    }
    return render(request, 'src/documentanalytique.html', context)

#===================================GENERER UN DOCUMENT ===================================#
def generedocument(request):
    tlettre = TypeLettre.objects.all()
    tbanque = TypeBanque.objects.all()
    context = {
        'tlettres':tlettre,
        'tbanques':tbanque,
    }
    return render(request, 'src/generedocument.html', context)

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
    Hformation = HFormation.objects.all()
    context = {
        'Hformations':Hformation
    }
    return render(request, 'src/historique.html', context)

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


def delete_conge(request, id):
    conge = Conge.objects.get(id=id)
    conge.delete()
    return redirect('conge')


def formation_terminer(request, id):
    print("je suis dedans")
    formationcours = get_object_or_404(Formation,id=id)
    print("je suis passe ici")
    try:

        formation = HFormation.create(formationcours)
        print("je suis passe encors ")
        formation.save()
        print("j'ai enregistrer")
    except:
        message_erreur = "Enregistrement échoué"
    formationcours.delete()
    return redirect('formationcours')
