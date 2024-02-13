# Application/urls.py
from django.urls import path
from .views import *
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
    path('documentcat', documentCAT, name='documentcat'), 
    path('documentanalytique', documentanalytique, name='documentanalytique'), 
    path('generedocument', generedocument, name='generedocument'), 
    path('genereDocL/<int:id>', genereDocL, name='genereDocL'), 
    path('genereDocB/<int:id>', genereDocB, name='genereDocB'), 
    path('detailspersonnel/<int:id>', detailspersonnel, name='detailspersonnel'), 
]
