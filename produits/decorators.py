from django.core.exceptions import PermissionDenied
from django.http import Http404

from utilisateurs.decorators import check_permissions_generique
from utilisateurs.methods import check_existence_element
from .models import *

def check_permissions_et_existance_produit():
    def decorator(func):
        def wrapper(request, id: int = None):
            produit = check_existence_element(Produit, id, retour=True, unique=True)
            if produit is None:
                raise Http404
            # elif request.user not in produit.accesproduit_set and not request.user.has_perm('peut_voir_produits_global'):
            #    raise PermissionDenied   ToDo : Checker la permission d'accès aux produits
            return func(request, id)
        return wrapper
    return decorator
