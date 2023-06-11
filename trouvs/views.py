from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404

from produits.models import Produit
from .forms import TrouvForm, TrouvFormModification, TrouvFormRapide, FichierTrouvForm
from .models import Trouv, Vote


def chargement_votes_utilisateur(utilisateur):
    votes = Vote.objects.filter(utilisateur=utilisateur)
    deja_aime = votes.filter(valeur=1).values_list('trouv', flat=True)
    deja_pas_aime = votes.filter(valeur=-1).values_list('trouv', flat=True)
    return votes, deja_aime, deja_pas_aime


@login_required(login_url='/connexion')
def index(request):
    votes = chargement_votes_utilisateur(request.user.utilisateur)
    return render(request, 'trouvs/pages/index.html', {
        'titre': 'Accueil',
        'trouvs': Trouv.objects.all().order_by('-date_creation'),
        'deja_aime': votes[1],
        'deja_pas_aime': votes[2],
        'session_utilisateur': request.user.utilisateur,
        'form_rapide': TrouvFormRapide(),
    })


@login_required(login_url='/connexion')
def listing(request):
    return render(request, 'trouvs/pages/listing.html', {
        'titre': 'Trouvs',
        'trouvs': Trouv.objects.all(),
        'session_utilisateur': request.user.utilisateur,
        'est_page_perso': False
    })


@login_required(login_url='/connexion')
def details(request, id_trouv: int):
    if not (trouv := Trouv.objects.filter(id=id_trouv)).exists():
        raise Http404
    else:
        trouv_a_afficher = trouv.first()
        votes = chargement_votes_utilisateur(request.user.utilisateur)
        est_proprietaire = request.user.utilisateur == trouv_a_afficher.utilisateur

        context = {
            'titre': 'Recherche de trouvs',
            'trouv': trouv_a_afficher,
            'deja_aime': votes[1],
            'deja_pas_aime': votes[2],
        }

        if est_proprietaire:
            context.update({
                'form_edition': TrouvFormModification(initial=trouv_a_afficher.__dict_form__()),
                'form_fichier': FichierTrouvForm(initial={'trouv': trouv_a_afficher})
            })

        return render(request, 'trouvs/pages/details.html', context)


@login_required(login_url='/connexion')
def creation(request):
    description = ''
    produit = None

    if request.method == 'POST' and (form := TrouvFormRapide(request.POST, request.FILES)).is_valid():
        description = form.cleaned_data['description']

    if 'id_produit' in request.GET and (produit := Produit.objects.filter(id=request.GET['id_produit'])).exists():
        produit = produit.first()

    return render(request, 'trouvs/pages/creer.html', {
        'titre': 'Créer un trouv',
        'form': TrouvForm(initial={'description': description, 'produit': produit}),
        'form_fichiers': FichierTrouvForm(),
        'produits': Produit.objects.filter(utilisateurs_abonnes__user=request.user),
        'description': description
    })


@login_required(login_url='/connexion')
def gestion(request):
    return render(request, 'trouvs/pages/listing.html', {
        'titre': 'Gestion des trouvs',
        'trouvs': Trouv.objects.filter(utilisateur__user=request.user),
        'est_page_perso': True
    })
