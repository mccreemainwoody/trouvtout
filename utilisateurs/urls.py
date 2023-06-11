from django.urls import path
from . import views

urlpatterns = [
    path('', views.profil, name='profil'),
    path('edition', views.edition_profil, name='edition_profil'),
    path('supprimer', views.supprimer_profil, name='supprimer_profil'),
    path('<int:id>', views.profil, name='profil'),
]
