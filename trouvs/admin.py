from django.contrib import admin

from .models import Trouv

# Register your models here.
@admin.register(Trouv)
class TrouvAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'produit', 'date_creation', 'date_modification', 'date_suppression')
    readonly_fields = ('utilisateur', 'produit', 'no_votes', 'date_creation', 'date_modification', 'date_suppression')
