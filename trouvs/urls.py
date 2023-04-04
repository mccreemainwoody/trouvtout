from django.urls import path
from . import views

urlpatterns = [
    path('', views.listing, name='listing'),
    path('produit/<int:id>', views.listing, name='listing_produit'),
    path('<int:id>', views.details, name='details', kwargs={'id': id}),
    path('creation', views.creation, name='creation'),
    path('gestion', views.gestion, name='gestion'),
    path('gestion/<int:id>', views.modification, name='modification'),
]