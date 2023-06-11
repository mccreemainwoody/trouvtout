from django.contrib import admin

from .models import Utilisateur


# Register your models here.
@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_creation', 'date_modification', 'date_suppression')
    list_filter = ('user', 'date_creation', 'date_modification', 'date_suppression')
    readonly_fields = ('user', 'date_creation', 'date_modification', 'date_suppression')
