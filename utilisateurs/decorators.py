from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import request, Http404

from .models import Utilisateur
from .methods import check_permissions_generique, check_existence_element
from utilisateurs.models import *


def check_permissions_utilisateur(permission: str = None):
    def decorator(func):
        def wrapper(request: request, id: int = None):
            raccourcis_permissions = {
                'voir': 'utilisateurs.peut_voir_utilisateurs_global',
                'editer': 'utilisateurs.peut_editer_utilisateurs_global',
                'supprimer': 'utilisateurs.peut_supprimer_utilisateurs_global'
            }
            recherche_permission = permission if permission is None else 'voir'
            id = request.user.id if id is None else id
            check_existence_element(Utilisateur, id)
            if id != request.user.id and not check_permissions_generique(request, raccourcis_permissions[recherche_permission]):
                raise PermissionDenied()
            return func(request, id)
        return wrapper
    return decorator

