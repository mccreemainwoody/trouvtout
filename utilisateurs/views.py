from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .decorators import *
from .methods import *


# Create your views here.
def connexion(request):
    if request.user.is_authenticated:
        return redirect('/')
    elif request.method != 'POST':
        return render(request, 'utilisateurs/auth/login.html')
    elif request.POST['username'] == '' or request.POST['password'] == '':
        messages.warning(request, "Veuillez remplir tous les champs !")
        return render(request, 'utilisateurs/auth/login.html')

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user.utilisateur.datesupp is None:
            login(request, user)
            return redirect('/')
        elif user.utilisateur.datesupp < datetime.now() - timedelta(days=30):
                messages.warning(request, "Désolé, ce compte a été supprimé il y a moins de 30 jours. Impossible "
                                          "de se connecter ! Si vous aviez des souhaits non accomplis sur ce compte, "
                                          "et être venu pour rétablir la paix dans l'âme de votre compte défunt, "
                                          "contactez un administrateur !")
    messages.warning(request, "Nom d\'utilisateur ou mot de passe incorrect")
    return render(request, 'utilisateurs/auth/login.html')


def deconnexion(request):
    if request.user.is_authenticated:
        logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès !")
    return redirect('utilisateurs:connexion')


def inscription(request):
    if request.method != 'POST':
        return render(request, 'utilisateurs/auth/register.html')

    nom = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    check_tout(request, nom=nom, password=password, password2=request.POST['confirm_password'], email=email)
    if messages.get_messages(request):
        return render(request, 'utilisateurs/auth/register.html')

    user = User.objects.create_user(nom, email, password)
    user.save()
    utilisateur = Utilisateur(user=user)
    utilisateur.save()
    login(request, user.user)
    return redirect('utilisateurs:connexion')


def mot_de_passe_oublie(request):
    # ToDo : Envoyer un mail avec un lien pour réinitialiser le mot de passe
    if request.method != 'POST':
        return render(request, 'utilisateurs/auth/forgot-password.html')
    return render(request, 'utilisateurs/auth/forgot-password.html')


def recuperation_mot_de_passe(request):
    # ToDo : Faire le processus de réinitialisation du mot de passe
    if request.method != 'POST':
        return render(request, 'utilisateurs/auth/recover-password.html')
    return render(request, 'utilisateurs/auth/recover-password.html')


@login_required(login_url='/connexion')
@check_permissions_utilisateur('utilisateurs.peut_voir_utilisateurs_global')
def profil(request, id=None):
    return render(request, 'utilisateurs/profil.html', {
        'titre': 'Profil',
        'utilisateur': request.user.utilisateur if id is None else Utilisateur.objects.get(id=id)
    })


@login_required(login_url='/connexion')
@check_permissions_utilisateur('utilisateurs.peut_editer_utilisateurs_global')
def edition_profil(request, id: int = None):
    utilisateur = request.user.utilisateur if id is None else Utilisateur.objects.get(id=id)
    contexte = {
        'titre': 'Edition de profil',
        'utilisateur': utilisateur
    }
    if request.method != 'POST':
        return render(request, 'utilisateurs/edition.html', contexte)

    modification = {key: value for key, value in request.POST.items()
                    if key != 'csrfmiddlewaretoken' and value != ''}

    check_tout(request, confirmation=True, **modification)
    if not messages.get_messages(request):  # Si la vérification n'a pas retourné d'avertissement
        a_retirer = [k for k in modification.keys()
                     if getattr(utilisateur, k, False) is False
                        and getattr(utilisateur.user, k, False) is False
                     or getattr(utilisateur.user, k) == modification[k]]
        [modification.pop(k) for k in a_retirer]
        utilisateur.update(**modification)
        messages.success(request, "Votre profil a été édité avec succès !")

    return render(request, 'utilisateurs/edition.html', contexte)


@login_required(login_url='utilisateurs:connexion')
def supprimer_profil(request, id=None):
    if request.method != 'POST':
        return render(request, 'utilisateurs/confirmation_suppression.html', {
            'titre': 'Suppression de profil',
            'utilisateur': Utilisateur.objects.get(id=request.user.id)
        })
    utilisateur = request.user.utilisateur if id is None else Utilisateur.objects.get(id=id)
    utilisateur.delete()
    messages.success(request, "Votre compte a été supprimé avec succès !")
    return redirect('utilisateurs:connexion')
