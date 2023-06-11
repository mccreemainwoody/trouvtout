from django import forms

from .models import Trouv, FichierTrouv
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
        }


class TrouvFormModification(forms.ModelForm):
    class Meta:
        model = Trouv
        fields = ['titre', 'description']
        labels = {
            'titre': 'Titre',
            'description': 'Description',
        }
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class FichierTrouvForm(forms.ModelForm):
    class Meta:
        model = FichierTrouv
        fields = ['trouv', 'fichier']
        labels = {
            'trouv': 'Trouv',
            'fichier': 'Fichiers',
        }
        widgets = {
            'trouv': forms.HiddenInput(),
            'fichier': forms.FileInput(attrs={'class': 'form-control-file form-ajout-fichier'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fichier'].required = False

    def clean_fichier(self):
        fichier = self.cleaned_data['fichier']
        if fichier:
            if fichier.size > 1024 * 1024 * 10:
                raise forms.ValidationError("Le fichier est trop volumineux ( > 10mb )")
            return fichier
        else:
            raise forms.ValidationError("Le fichier est invalide")


class TrouvFormRapide(forms.ModelForm):
    class Meta:
        model = Trouv
        fields = ['description']
        labels = {
            'description': 'Qu\'allez-vous créer aujourd\'hui ?',
        }
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
