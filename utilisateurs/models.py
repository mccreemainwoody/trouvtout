from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    banniere = models.ImageField(upload_to='banniere', null=True, blank=True)
    datecrea = models.DateTimeField(auto_now_add=True)
    datemodif = models.DateTimeField(auto_now=True, null=True, blank=True)
    datesupp = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'utilisateurs'
        ordering = ['user']
        permissions = [
            ('peut_voir_trouvs_global', 'Peut voir tous les trouvs du produit, indépéndamment du suivi de leur produit.'),
            ('peut_creer_trouvs_global', 'Peut créer des trouvs pour tous les produits, indépendamment de leur suivi.'),
            ('peut_modifier_trouvs_global', 'Peut modifier n\'importe quel trouv.'),
            ('peut_supprimer_trouvs_global', 'Peut supprimer n\'importe quel trouv.'),
            ('peut_voir_produits_global', 'Peut voir tous les produits, indépendamment de leur suivi.'),
            ('peut_creer_produits_global', 'Peut créer des produits.'),
            ('peut_modifier_produits_global', 'Peut modifier n\'importe quel produit.'),
            ('peut_supprimer_produits_global', 'Peut supprimer n\'importe quel produit.'),
            ('peut_voir_utilisateurs_global', 'Peut voir tous les utilisateurs.'),
            ('peut_creer_utilisateurs_global', 'Peut créer des utilisateurs sur la plateforme admin.'),
            ('peut_modifier_utilisateurs_global', 'Peut modifier n\'importe quel utilisateur.'),
            ('peut_supprimer_utilisateurs_global', 'Peut supprimer ,\'importe quel utilisateur.'),
        ]

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return self.__str__()

    def delete(self, using=None, keep_parents=False):
        self.datesupp = timezone.now()
        self.save()

    def update(self, **kwargs):
        keys = [k for k in kwargs.keys() if k in ['username', 'email', 'password', 'first_name', 'last_name']]
        self.update_user(**{k: kwargs.pop(k) for k in keys})
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.datemodif = timezone.now()
        self.save()

    def update_user(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self.user, key, value)
        print(self.user.username, self.user.email, self.user.password, self.user.first_name, self.user.last_name)
        self.user.save()
