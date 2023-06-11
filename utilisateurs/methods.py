from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404

min_caracteres_nom, min_caracteres_mdp = 5, 8


def check_tout(request, confirmation=False, **kwargs):
    if 'nom' in kwargs:
        check_nom(request, kwargs['nom'])
    if confirmation:
        check_mdp_confirmation(request, '' if 'mdp_confirmation' not in kwargs else kwargs['mdp_confirmation'])
    if 'password' in kwargs:
        check_mdp(request, kwargs['mdp'], '' if 'mdp2' not in kwargs else kwargs['mdp2'])
    if 'email' in kwargs:
        check_email(request, kwargs['email'])
    if 'banniere' in kwargs:
        check_banniere(request, kwargs['banniere'])


def check_tout_inscription(request, **kwargs):
    check_tout(request, **kwargs)
    check_terms(request)


def check_terms(request):
    if 'terms' not in request.POST or request.POST['terms'] != 'agree':
        messages.warning(request, "Vous n'avez pas accepté les conditions d'utilisation. "
                                  "Acceptez-les avant de vous inscrire ! (faites-le, c'est important)")


def check_nom(request, nom):
    if len(nom) < min_caracteres_nom:
        messages.warning(request, "Votre nom d\'utilisateur est trop court. "
                                  "Essayez d'atteindre au minimum 5 caractères !")
    if User.objects.filter(username=nom).exists():
        messages.warning(request, "Oh oh, ce nom d\'utilisateur est déjà pris !")


def check_mdp(request, mdp, mdp2):
    if mdp != mdp2:
        messages.warning(request, "Oh non, on dirait que les mots de passe ne correspondent pas. :c")
    if len(mdp) < min_caracteres_mdp:
        messages.warning(request, "Votre mot de passe est trop court. Essayez de l'agrandir un peu !")
    if mdp.isalpha() or mdp.isdigit():
        messages.warning(request, "Votre mot de passe n'est composé que de chiffres ou de lettres. "
                                  "Faites comme dans une bonne salade et tentez de mélanger des chiffres "
                                  "et des lettres !")
    if mdp.islower() or mdp.isupper():
        messages.warning(request, "Votre mot de passe n'est composé que de lettres minuscules ou de lettres "
                                  "majuscules. C'est une bonne base, mais c'est toujours important de faire "
                                  "un peu de mixité dans un mot de passe. Essayez avec des lettres minuscules "
                                  "et des lettres majuscules !")


def check_email(request, email):
    if User.objects.filter(email=email).exists() and (request.user is None or request.user.email != email):
        messages.warning(request, "Oh oh, cette adresse email est déjà utilisée !")


def check_banniere(request, banniere):
    if banniere.size > 2000000:
        messages.warning(request, "Votre bannière est trop volumineuse. Essayez de la réduire un peu !")


def check_mdp_confirmation(request, mdp):
    if not request.user.check_password(mdp):
        messages.warning(request, "Oh non, on dirait que le mot de passe que vous avez entré n'est pas le bon. :c")


@login_required(login_url='/connexion')
def check_permissions_generique(request, permission, exception_si_echec: bool = False) -> bool:
    if request.user.has_perm(permission):
        return True
    if exception_si_echec:
        raise PermissionDenied
    return False


def check_existence_element(modele, id: int, retour: bool = False, unique: bool = False) -> object | None:
    recherche = modele.objects.filter(id=id)
    if not recherche:
        raise Http404
    return None if not retour else recherche if not unique else recherche.first()
