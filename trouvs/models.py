from django.db import models


# Create your models here.
class Trouv(models.Model):
    id = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=100)
    description = models.TextField(max_length=2500, null=True, blank=True)
    utilisateur = models.ForeignKey('utilisateurs.Utilisateur', on_delete=models.CASCADE)
    produit = models.ForeignKey('produits.Produit', on_delete=models.CASCADE)
    votes = models.ManyToManyField('utilisateurs.Utilisateur', through='Vote', related_name='votes')
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


class Vote(models.Model):
    utilisateur = models.ForeignKey('utilisateurs.Utilisateur', on_delete=models.CASCADE)
    trouv = models.ForeignKey('Trouv', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'votes'
        unique_together = ('utilisateur', 'trouv')

    def __str__(self):
        return f"{self.utilisateur} a voté pour {self.trouv} !"


class FichiersTrouv(models.Model):
    trouv = models.ForeignKey('Trouv', on_delete=models.CASCADE)
    fichier = models.FileField(upload_to='fichiers')

    class Meta:
        db_table = 'fichiers_trouv'
        unique_together = ('trouv', 'fichier')

    def __str__(self):
        return self.fichier.name
