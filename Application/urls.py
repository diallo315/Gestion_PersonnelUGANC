# Application/urls.py
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', loginsignup, name='loginsignup'),
    path('dashboard', dashboard, name='dashboard'),
    path('personnel', personnel, name='personnel'),
    #path('ajoutpersonnel', ajoutpersonnel, name='ajoutpersonnel'),
    path('document', doucument, name='document'),
    path('formationcours', formationcours, name='formationcours'),
    path('historique', historique, name='historique'),
    path('inscritformation', inscritformation, name='inscritformation'),
    path('conge', conge, name='conge'), 
    path('ajoutconge', ajoutconge, name='ajoutconge'), 
    path('categorieag/<int:id>', categorieag, name='categorieag'), 
    path('documentcat/<int:id>', documentCAT, name='documentcat'), 
    path('documentanalytique', documentanalytique, name='documentanalytique'), 
    path('generedocument', generedocument, name='generedocument'), 
    path('genereDocL/<int:id>', genereDocL, name='genereDocL'), 
    path('genereDocB/<int:id>', genereDocB, name='genereDocB'), 
    path('detailspersonnel/<int:id>', detailspersonnel, name='detailspersonnel'),
    path('ajoutdocument/<int:id>', ajoutdocument, name='ajoutdocument'),
    path('typedocument/<int:id>', typedocument, name='typedocument'),
    path('delconge/<int:id>/',delete_conge,name="delete_conge"),
    path('formationTer/<int:id>/', formation_terminer, name="formation_terminer")
]

# Ajouter ces lignes pour servir les fichiers médias pendant le développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
