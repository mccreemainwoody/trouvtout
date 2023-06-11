from django.contrib import admin

from .models import Produit


# Register your models here.
@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    pass
