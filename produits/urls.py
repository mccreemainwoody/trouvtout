from django.urls import path
from . import views

urlpatterns = [
    path('', views.listing, name='listing'),
    path('<int:id>', views.details, name='details'),
    path('suivis', views.listing_abonnes, name='listing_abonnes'),
]
