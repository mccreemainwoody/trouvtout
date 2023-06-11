from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import Http404
from .models import Produit
from .decorators import check_permissions_et_existance_produit


@login_required(login_url='/connexion')
def listing(request):
    return render(request, 'produits/listing.html', {
        'titre': 'Produits',
        'produits': Produit.objects.all()
    })


@login_required(login_url='/connexion')
def listing_abonnes(request):
    return render(request, 'produits/listing.html', {
        'titre': 'Produits suivis',
        'produits': Produit.objects.filter(utilisateurs_abonnes__user=request.user)
    })


@login_required(login_url='/connexion')
@check_permissions_et_existance_produit()
def details(request, id):
    produit = Produit.objects.get(id=id)
    return render(request, 'produits/details.html', {
        'titre': 'Recherche de produits',
        'produit': produit,
        'trouvs': produit.trouv_set.all().order_by('-date_creation')
    })
