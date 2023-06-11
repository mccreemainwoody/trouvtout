from django.db import models
from django.utils import timezone


# Create your models here.
class Trouv(models.Model):
    id = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=100)
    description = models.TextField(max_length=2500, null=True, blank=True)
    utilisateur = models.ForeignKey('utilisateurs.Utilisateur', on_delete=models.CASCADE)
    produit = models.ForeignKey('produits.Produit', on_delete=models.CASCADE)
    votes = models.ManyToManyField('utilisateurs.Utilisateur', through='Vote', related_name='votes')
    no_votes = models.IntegerField(default=0)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True, null=True, blank=True)
    date_suppression = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'trouvs'
        ordering = ['id']
        permissions = [
            ('peut_voir', 'Peut voir le trouv, indépendamment de son produit'),
            ('peut_modifier_trouv', 'Peut modifier le trouv.'),
            ('peut_supprimer_trouv', 'Peut supprimer le trouv.'),
        ]

    def __str__(self):
        return self.titre

    def __dict_form__(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'description': self.description
        }

    def delete_by_date(self):
        Vote.objects.filter(trouv=self).delete()
        FichierTrouv.objects.filter(trouv=self).delete()
        self.date_suppression = timezone.now()
        self.save()


class Vote(models.Model):
    class PoucesPossibles(models.IntegerChoices):
        pouce_bleu = 1
        pouce_rouge = -1

    valeur = models.IntegerField(choices=PoucesPossibles.choices)
    utilisateur = models.ForeignKey('utilisateurs.Utilisateur', on_delete=models.CASCADE)
    trouv = models.ForeignKey('Trouv', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'votes'
        unique_together = ('utilisateur', 'trouv')

    def __str__(self):
        return f"{self.utilisateur} a voté pour {self.trouv} !"


class FichierTrouv(models.Model):
    trouv = models.ForeignKey('Trouv', on_delete=models.CASCADE)
    fichier = models.FileField(upload_to='fichiers')

    class Meta:
        db_table = 'fichiers_trouv'
        unique_together = ('trouv', 'fichier')

    def __str__(self):
        return self.fichier.name

    def delete(self, using=None, keep_parents=False):
        self.fichier.delete()
        super().delete(using=using, keep_parents=keep_parents)
