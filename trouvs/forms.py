from django import forms

from .models import Trouv
from produits.models import Produit


class TrouvForm(forms.ModelForm):
    class Meta:
        model = Trouv
        fields = ['titre', 'description', 'produit']
        labels = {
            'titre': 'Titre',
            'description': 'Description',
            'produit': 'Produit affilié',
        }
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'produit': forms.Select(attrs={'class': 'form-control'}, choices=Produit.objects.all()),
            'fichiers': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
