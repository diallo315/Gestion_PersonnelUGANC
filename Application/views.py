# Application/views.py
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout, get_user_model


import matplotlib
matplotlib.use('Agg')

#==========================CONNEXION ET INSCRIPTION ==============================#
def loginsignup(request):
    mot_de_pass_incoherent = ""
    Utilisateur_exist_deja = ""
    connexion_echouer = ""

    if request.method == "POST":
        try:
            is_connexion = request.POST.get("is_connexion")
            # print(is_connexion)
            if is_connexion == 'on':
                emailrecu = request.POST.get("mail")
                password1 = request.POST.get("password1")
                user_connect = authenticate(request, username=emailrecu, password=password1)
                
                if user_connect:
                    # print("j'ai authentifie " + emailrecu + " avec le mot de passe "+ password1)
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
    is_cat = False
    if request.method == "POST":
        cat = request.POST.get('cat')
        searchField = request.POST.get('searchField')
        if cat == 'ag':
            administrationGeneral = AdministrationGeneral.objects.filter(nom=searchField)
            personnel = Personnel.objects.all()
            categorie = Categorie.objects.all()
        elif cat == 'matricule':
            personnel = Personnel.objects.get(matricule=searchField)
            return detailspersonnel(request, personnel.id)
        elif cat == 'faculte':
            administrationGeneral =  ""
            categorie = Categorie.objects.filter(nomcategorie=searchField)
            categorie_ids = categorie.values_list('id', flat=True)  # Extraire les IDs des catégories filtrées
            personnel = Personnel.objects.filter(categorie__in=categorie_ids)
            is_cat = True
        else:
            administrationGeneral = AdministrationGeneral.objects.all()
            personnel = Personnel.objects.all()
            categorie = Categorie.objects.all()
    else:
        administrationGeneral = AdministrationGeneral.objects.all()
        personnel = Personnel.objects.all()
        categorie = Categorie.objects.all()
    
    context = {
        'is_cat': is_cat,
        'personnels' : personnel, 
        'administrationGenerals' : administrationGeneral,
        'categories': categorie,
    }
    return render(request, 'src/personnels/personnel.html', context)

#==================================DETAILS D'UN PERSONNEL ============================================#
def detailspersonnel(request, id):
    personnel = Personnel.objects.get(id = id)
    context = {
        'personnel' : personnel, 
    }
    return render(request, 'src/personnels/detailspersonnel.html.', context)


#===============================DOCUMENT ===================================================#
def doucument(request):
    administrationGeneral = AdministrationGeneral.objects.all()
    context = {
        'administrationGenerals' : administrationGeneral,
    }
    return render(request, 'src/documents/document.html', context)

#===============================TYPE DE DOCUMENT ===================================================#
def typedocument(request, id):
    typedocument = TypeDocument.objects.all()
    categorie = Categorie.objects.get(id = id)
    context = {
        'typedocuments' : typedocument,
        'categorie' : categorie,
    }
    return render(request, 'src/documents/typedocument.html', context)

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
                return render(request, 'src/documents/documentCAT.html', {'message_succes': message_success})
            else:
                matricule_exist = "Cette personne n'existe dans votre Base donnée"
        else:
            accept = "Confirmé l'ajout du Document"
    context = {
        'typedocument' : typedocument,
        'matricule_exist':matricule_exist,
        'accept': accept,
    }
    return render(request, 'src/documents/ajoutdocument.html', context)

#===============================DOCUMENT ADMINISTRATIF GENERAL ===================================================#
def categorieag(request, id):
    administrationgeneral = AdministrationGeneral.objects.get(id = id)
    categorie = Categorie.objects.filter(administrationGeneral = administrationgeneral)
    context = {
        'categories' : categorie,
        'administrationgeneral' : administrationgeneral,
    }
    return render(request, 'src/personnels/categorieAG.html', context)

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
    return render(request, 'src/documents/documentCAT.html', context)

#===============================DOCUMENT GENERE ===================================================#
def genereDocL(request, id):
    message_success=""
    tlettre = TypeLettre.objects.get(id=id)
    personnels = Personnel.objects.all()
    context = {
        'tlettre' : tlettre,
        'matricules' : personnels,
        'message_success': message_success

    }
    
    if request.method == "POST":
        matricule = request.POST.get("matricule")
        dateJour = request.POST.get("dateJour")
        personnel = Personnel.objects.get(matricule = matricule)
        lettre = Lettre(
            personnel = personnel,
            typelettre = tlettre,
            datejour = dateJour
        )
        lettre.save()
        message_success = "Enregistres avec succès ! "
        return render(request, 'src/documents/genereDocL.html', {'message_success': message_success})
    
    return render(request, 'src/documents/genereDocL.html', context)

#===============================DOCUMENT GENERE ===================================================#
def genereDocB(request, id):
    message_success =""
    tbanque = TypeBanque.objects.get(id=id)
    personnels = Personnel.objects.all()
    context = {
        'tbanque': tbanque,
        'matricules': personnels,
        'message_success': message_success
    }

    if request.method == "POST":
        matricule = request.POST.get("matricule")
        nomBanque = request.POST.get("nombanque")
        numeroBanque = request.POST.get("numerobanque")
        datejour = request.POST.get("dateJour")
        personnel = Personnel.objects.get(matricule = matricule)
        lettreBanque = LettreBanque(
            personnel = personnel,
            nombanque = nomBanque,
            numerobanque = numeroBanque,
            typebanque = tbanque,
            datejour = datejour
        )
        lettreBanque.save()
        message_success = "Enregistré avec succès ! "
        return render(request, 'src/documents/genereDocB.html', {'message_success': message_success})

    return render(request, 'src/documents/genereDocB.html', context)

#===================================DOCUMENT ANALYTIQUE===================================#
def documentanalytique(request):
    tlettre = TypeLettre.objects.all()
    tbanque = TypeBanque.objects.all()
    context = {
        'tlettres':tlettre,
        'tbanques':tbanque,
    }
    return render(request, 'src/documents/documentanalytique.html', context)

#===================================DETAIL DOCUMENT ANALYTIQUE LETTRE===================================#
def detailAnalytiqueL(request, id):
    tlettre = TypeLettre.objects.get(id= id)
    lettre = Lettre.objects.filter(typelettre = tlettre)
    trouve = len(lettre) > 0 
    context = {
        'lettres':lettre,
        'trouver': trouve,
        'tlettre': tlettre
    }
    return render(request, 'src/documents/detailDocAnalytiqueL.html', context)
#===================================DOCUMENT ANALYTIQUE===================================#
def detailAnalytiqueB(request, id):
    tbanque = TypeBanque.objects.get(id=id)
    lettreBancaire = LettreBanque.objects.filter(typebanque = tbanque)
    trouve = len(lettreBancaire) > 0
    context = {
        'lettrebancaires':lettreBancaire,
        'trouver': trouve,
        'tbanque': tbanque
    }
    return render(request, 'src/documents/detailDocAnalytiqueB.html', context)

#===================================GENERER UN DOCUMENT ===================================#
def generedocument(request):
    tlettre = TypeLettre.objects.all()
    tbanque = TypeBanque.objects.all()
    context = {
        'tlettres':tlettre,
        'tbanques':tbanque,
    }
    return render(request, 'src/documents/generedocument.html', context)

#==========================================CONGE ======================================#
def conge(request):
    if request.method == "POST":
        search_text = request.POST.get('search_text')
        recherche = request.POST.get('values')
        if recherche == "matricule":
            personnel = Personnel.objects.get(matricule = search_text)
            conge = Conge.objects.filter(personnel = personnel)
        elif recherche == "typeconges":
            conge = Conge.objects.filter(typeconges = search_text)
        else :
            conge = Conge.objects.all()
    else:
        conge = Conge.objects.all()
        
       
    context = { 
        'conges':conge,
    }
    return render(request, 'src/conges/conge.html', context)

#==========================================AJOUT D'UN CONGE ======================================#
def ajoutconge(request):
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
            return render(request, 'src/conges/conge.html', {'conges_success':conges_success})
       except:
           pass
       
    return render(request, 'src/conges/ajoutconge.html')

#===================================INSCRIPTION A UNE FORMATION ===================================#
def inscritformation(request):
    return render(request, 'src/formations/inscritformation.html')

#===================================HISTORIQUE ========================================================#
def historique_formation(request):

    if request.method == "POST":
        cond_recherche = request.POST.get('values')
        recherche = request.POST.get('search_text')
        if cond_recherche == "matricule":
            personnel = Personnel.objects.get(matricule = recherche)
            Hformation = HFormation.objects.filter(personnel = personnel)
        elif cond_recherche == "programmeformation":
            pFormation = ProgrammeFormation.objects.filter(nom = recherche)
            Hformation = HFormation.objects.filter(programmeFormation__in = pFormation)
        else:
            Hformation = HFormation.objects.all()
    else:
        Hformation = HFormation.objects.all()
    context = {
        'Hformations':Hformation
    }
    return render(request, 'src/formations/historiqueFormation.html', context)

#=========================================FORMATIONS EN COURS =========================================#
def formationcours(request):
    message_erreur = ""
    message_success = ""
    if request.method == "POST":
        checked = request.POST.get('is_check')
        if checked:
            cond_recherche = request.POST.get('values')
            recherche = request.POST.get('search_text')
            if cond_recherche == "matricule":
                personnel = Personnel.objects.get(matricule = recherche)
                formation = Formation.objects.filter(personnel = personnel)
            elif cond_recherche == "programmeformation":
                pFormation = ProgrammeFormation.objects.filter(nom = recherche)
                formation = Formation.objects.filter(programmeFormation__in = pFormation)
            else:
                formation = Formation.objects.all()
        else:
            programmeFormation = request.POST.get('formationEncours')
            print(programmeFormation)
            if programmeFormation == "none":
                message_erreur = "Aucune formation n'a été selectionne ! "
            else:
                programmeFormationTrouve = ProgrammeFormation.objects.get(id = programmeFormation)
                print(programmeFormationTrouve)
                formationTerminer = Formation.objects.filter(programmeFormation = programmeFormationTrouve)
                print(formationTerminer)
                for formation in formationTerminer:
                    hFormation, created = HFormation.objects.get_or_create(
                        personnel=formation.personnel, 
                        programmeFormation = formation.programmeFormation,
                        defaults={"observation": "Formation " + str(programmeFormationTrouve) + " terminée."}
                    )
                    if created:
                        print(created)
                        hFormation.save()

                    # Supprimer la formation de la base de données
                    formation.delete()
                formation = Formation.objects.all()
                message_success = "Formation terminée avec succès !"
    else:
        formation = Formation.objects.all()
    
    programmes_formation_ids = Formation.objects.values_list('programmeFormation', flat=True).distinct()
    programmes_formation = ProgrammeFormation.objects.filter(id__in=programmes_formation_ids)

    context = {
        'programmes_formation': programmes_formation,
        'formations': formation,
        'message_erreur': message_erreur,
        'message_success': message_success
    }
    return render(request, 'src/formations/formationcours.html', context)
#=========================================DECONNEXION  =========================================#
def templates(request):
    messageDeconnexion = ""
    if request.method == 'POST':
        deconnexion = request.POST.get('is_deconnect')
        print("JE SUIS DEDANS ET VOICI L'ETAT DE DECONNEXION " + deconnexion )
        if deconnexion == 'on':
            messageDeconnexion = "Merci d'avoir connsulter l'application "
            return render(request, 'src/loginSignup.html', {'messageDeconnexion': messageDeconnexion})
    return render(request, 'template.html')

#=========================================SUPPRIME UN CONGE ET SAVE HCONGE =========================================#

def conge_fini(request, id):
    conge = Conge.objects.get(id=id)
    hConge = HConge(
        personnel = conge.personnel,
        typeconges = conge.typeconges,
        dateDeb = conge.dateDeb, 
        dateFin = conge.dateFin, 
        observation = "validé"
    )
    hConge.save()
    conge.delete()
    return redirect('conge')

#=========================================SUPPRIME UN CONGE ET SAVE HCONGE =========================================#

def delete_hformation(request, id):
    Hformation = HFormation.objects.get(id=id)
    Hformation.delete()
    return redirect('historique')

# ====================================== HISTORIQUE DE CONGE ==============================

def historique_conge(request):
    if request.method == "POST":
        cond_recherche = request.POST.get('values')
        recherche = request.POST.get('search_text')
        if cond_recherche == "matricule": 
            personnel = Personnel.objects.get(matricule = recherche)
            hconge = HConge.objects.filter(personnel = personnel)
        elif cond_recherche == "typeconges": 
            hconge = HConge.objects.filter(typeconges = recherche)
        else:
            hconge = HConge.objects.all()
    else:
        hconge = HConge.objects.all()
    context = {
        'hconges': hconge
    }
    return render(request, 'src/conges/historiqueConges.html', context)


# ====================================== DECONNEXION  ==============================
def deconnexion(request):
    logout(request)
    return redirect('loginsignup')


# ====================================== TEST POUR AFFICHER LE VIEW ==============================
def View_detail_personne(request):
    return render(request, 'src/pdf/detailPersonnel.html.twig')


    