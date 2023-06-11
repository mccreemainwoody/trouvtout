from django.urls import path, include
from django.conf import settings

from . import views_api

urlpatterns = [
    path('modification', views_api.modification),
    path('suppression', views_api.suppression),
    path('pouce', views_api.pouce),
    path('ajout-fichier-trouv', views_api.ajout_fichier),
    path('suppression-fichier-trouv', views_api.suppression_fichier)
]
