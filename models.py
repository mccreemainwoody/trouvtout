# Organisation des modèles
# =============================================================================
# x - acces_produits - Produits
# ? - droits_systeme - Utilisateurs - A voir : Dans un groupe ou dans un modèle ?
#       - Envisager : Une classe enfant de User (ou de Group, oui si tu veux Copilot)
#       - https://docs.djangoproject.com/fr/4.1/topics/auth/customizing/#extending-user
# | - droits_produits - Dans le modèle Produit
#       - Est généré par Django avec django.contrib.auth.models.Group et le système
#       de permissions de Django. Lien pratique : https://www.honeybadger.io/blog/django-permissions/
#       - Remarque : Il va peut-être falloir créer des décorateurs personnalisés en créant un fichier
#       decorateur.py dans le dossier "utilisateurs" pour gérer les permissions.
#       - Pour créer des permissions (et les attribuer à un groupe) :
#       https://docs.djangoproject.com/en/4.1/topics/auth/default/#permissions-and-authorization
#           - Fixer les permissions du modèle
#           - Aller dans l'admin de Django
#           - Créer un groupe. Il sera possible de fixer les permissions du groupe pendant sa création.
# | - fichier - Géré par Django avec django.core.files.FileField
# x - produit - Produit
# x - trouv - Trouv
# | - utilisateur - Géné par Django avec django.contrib.auth.models.User
# x - vote - Trouv
#       - Envisager à mettre un compte de votes en plus du modèle Vote
# =============================================================================
# --> 4-5 modèles, 2 dans l'app Trouvs, 2 dans Produits, 1 dans Utilisateurs
# =============================================================================
