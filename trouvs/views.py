from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from utilisateurs.decorators import check_permissions_utilisateur
from produits.models import Produit
from .forms import TrouvForm
from .models import Trouv, FichiersTrouv


@login_required(login_url='/connexion')
def index(request):
    return render(request, 'trouvs/index.html', {
        'titre': 'Accueil',
        'trouvs': Trouv.objects.filter(produit__utilisateurs_abonnes__user=request.user)
    })


@login_required(login_url='/connexion')
def listing(request, id: int = None):
    try:
        produit = None if id is None else Produit.objects.filter(id=id)
        return render(request, 'trouvs/listing.html', {
            'titre': 'Trouvs',
            'produit': produit,
            'trouvs': Trouv.objects.filter(produit__utilisateurs_abonnes__user=request.user)
                      if produit else Trouv.objects.filter(produit=produit)
        })
    except Produit.DoesNotExist:
        raise Http404


@login_required(login_url='/connexion')
def details(request, id):
    trouv = Trouv.objects.filter(id=id)
    if trouv is None:
        raise Http404
    return render(request, 'trouvs/details.html', {
        'titre': 'Recherche de trouvs',
        'trouv': Trouv.objects.filter(id=id)
    })


@login_required(login_url='/connexion')
def creation(request):
    if request.method != 'POST':
        form = TrouvForm(request.POST, request.FILES)
        if form.is_valid():
            trouv = form.save(commit=False)
            trouv.utilisateur = request.user.utilisateur
            trouv.save()
            for fichier in request.FILES.getlist('fichiers'):
                FichiersTrouv.objects.create(trouv=trouv, fichier=fichier)
            return redirect('gestion')

    return render(request, 'trouvs/creer.html', {
        'titre': 'Créer un trouv',
        'form': TrouvForm(),
        'produits': Produit.objects.filter(utilisateurs_abonnes__user=request.user),
        'perso': True
    })


@login_required(login_url='/connexion')
def modification(request):
    if request.method != 'POST':
        pass
    redirect('gestion')


@login_required(login_url='/connexion')
def gestion(request):
    return render(request, 'trouvs/listing.html', {
        'titre': 'Gestion des trouvs',
        'trouvs': Trouv.objects.filter(utilisateur__user=request.user),
        'perso': True
    })
