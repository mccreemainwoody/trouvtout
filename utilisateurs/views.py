from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Utilisateur
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
        if user.utilisateur.date_suppression is None:
            login(request, user)
            return redirect('/')
        elif user.utilisateur.date_suppression < datetime.now() - timedelta(days=30):
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
    return redirect('/connexion')


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
def profil(request, id=None):
    if id is None:
        utilisateur = request.user.utilisateur
    else:
        utilisateur = Utilisateur.objects.filter(id=id)
        if not utilisateur.exists():
            return Http404
        utilisateur = utilisateur.first()

    return render(request, 'utilisateurs/profil.html', {
        'titre': 'Profil',
        'utilisateur': utilisateur
    })


@login_required(login_url='/connexion')
def edition_profil(request):
    utilisateur = request.user.utilisateur
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


@login_required(login_url='/connexion')
def supprimer_profil(request):
    utilisateur = request.user.utilisateur

    if request.method != 'POST':
        return render(request, 'utilisateurs/confirmation_suppression.html', {
            'titre': 'Suppression de profil',
            'utilisateur': utilisateur
        })

    utilisateur.delete_by_date()
    messages.success(request, "Votre compte a été supprimé avec succès !")
    return redirect('/connexion')
