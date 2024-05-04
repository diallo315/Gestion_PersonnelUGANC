from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import base64

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
