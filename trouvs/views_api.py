from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import redirect

from .models import Trouv, Vote, FichierTrouv
from .forms import TrouvForm, TrouvFormModification, FichierTrouvForm


def execution_fonction_api(envoi_data: bool = False, methodes: list[str] = None) -> callable:
    def wrapper(func: callable):
        def inner(request, *args, **kwargs):
            if envoi_data and request.method not in methodes:
                return HttpResponseBadRequest()
            try:
                return func.__call__(request, *args, **kwargs)
            except (KeyError, ValueError, ValidationError):
                return HttpResponseBadRequest()

        return inner

    return wrapper


@execution_fonction_api(envoi_data=True, methodes=['POST'])
@login_required(login_url='/connexion')
def creation(request):
    formulaire = TrouvForm(request.POST, request.FILES)
    formulaire_fichier = FichierTrouvForm(request.POST, request.FILES)
    if not formulaire.is_valid():
        return HttpResponseBadRequest

    trouv = formulaire.save(commit=False)
    trouv.utilisateur = request.user.utilisateur
    trouv.save()

    formulaire_fichier = formulaire_fichier
    formulaire_fichier.save()

    return HttpResponse(status=200)


@execution_fonction_api(envoi_data=True, methodes=['POST'])
@login_required(login_url='/connexion')
def modification(request):
    id_trouv = int(request.POST['id'])
    trouv = Trouv.objects.filter(id=id_trouv)
    if not trouv.exists():
        return HttpResponseNotFound()

    trouv = trouv.first()
    if request.user.utilisateur != trouv.utilisateur:
        return HttpResponseForbidden()

    formulaire = TrouvFormModification(request.POST)

    if not formulaire.is_valid():
        return HttpResponseBadRequest()

    trouv_modifie = formulaire.save(commit=False)
    trouv.titre = trouv_modifie.titre
    trouv.description = trouv.description
    trouv.save()

    return HttpResponse(status=200)


@execution_fonction_api(envoi_data=True, methodes=['GET'])
@login_required(login_url='/connexion')
def suppression(request):
    id_trouv = int(request.GET['id'])
    redirection = int(request.GET['redirection'])

    trouv = Trouv.objects.filter(id=id_trouv)
    if not trouv.exists():
        return HttpResponseNotFound()

    trouv = trouv.first()

    if request.user.utilisateur != trouv.utilisateur:
        return HttpResponseForbidden()

    trouv.delete_by_date()
    message = 'Le trouv a bien été supprimé !'

    return redirect('/') if redirection else HttpResponse(status=200, content=message)


@execution_fonction_api(envoi_data=True, methodes=['GET'])
@login_required(login_url='/connexion')
def pouce(request):
    user = request.user.utilisateur
    trouv_id, valeur = int(request.GET['trouv']), int(request.GET['valeur'])

    trouv = Trouv.objects.filter(id=trouv_id)
    if not trouv.exists():
        return HttpResponseNotFound()

    trouv = trouv.first()
    vote_existant = Vote.objects.filter(trouv=trouv, utilisateur=user)

    if not vote_existant.exists():
        nouveau_vote = Vote.objects.create(utilisateur=user, trouv=trouv, valeur=valeur)
        nouveau_vote.clean_fields()
        nouveau_vote.save()
        return HttpResponse(status=200, content=trouv.no_votes)

    vote_existant = vote_existant.first()
    if valeur == 0:
        vote_existant.delete()
    else:
        vote_existant.valeur = valeur
        vote_existant.clean_fields()
        vote_existant.save()

    return HttpResponse(status=200, content=trouv.no_votes)


@execution_fonction_api(envoi_data=True, methodes=['POST'])
@login_required(login_url='/connexion')
def ajout_fichier(request):
    id_trouv = int(request.POST['id_trouv'])

    trouv = Trouv.objects.filter(id=id_trouv)
    if not trouv.exists():
        return HttpResponseNotFound()

    trouv = trouv.first()
    if request.user.utilisateur != trouv.utilisateur:
        return HttpResponseForbidden()

    request.POST = request.POST.copy()
    request.POST['trouv'] = trouv

    formulaire = FichierTrouvForm(request.POST, request.FILES)
    if not formulaire.is_valid():
        return HttpResponseBadRequest(content=formulaire.errors)

    formulaire.save()

    return HttpResponse(status=200)


@execution_fonction_api(envoi_data=True, methodes=['GET'])
@login_required(login_url='/connexion')
def suppression_fichier(request):
    id_fichier = int(request.GET['id_fichier'])
    id_trouv = int(request.GET['id_trouv'])

    trouv = Trouv.objects.filter(id=id_trouv)
    if not trouv.exists():
        return HttpResponseNotFound()

    fichier = FichierTrouv.objects.filter(id=id_fichier, trouv=trouv.first())
    if not fichier.exists():
        return HttpResponseNotFound()

    fichier = fichier.first()

    if request.user.utilisateur != fichier.trouv.utilisateur:
        return HttpResponseForbidden()

    fichier.delete()
    return HttpResponse(status=200)
