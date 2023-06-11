from django.urls import path
from . import views

urlpatterns = [
    path('', views.listing, name='listing'),
    path('<int:id_trouv>', views.details, name='details'),
    path('creation', views.creation, name='creation'),
    path('gestion', views.gestion, name='gestion'),
]
