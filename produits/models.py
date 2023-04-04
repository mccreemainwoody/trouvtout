from django.db import models


class Produit(models.Model):
    nom = models.CharField(max_length=150, unique=True)
    description = models.TextField(max_length=1500, null=True, blank=True)
    photo_de_profil = models.ImageField(upload_to='pdp', null=True, blank=True)
    banniere = models.ImageField(upload_to='banniere', null=True, blank=True)
    utilisateurs_abonnes = models.ManyToManyField('utilisateurs.Utilisateur', through='AccesProduit')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True, null=True, blank=True)
    date_suppresion = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'produits'
        ordering = ['nom']
        permissions = [
            ('peut_voir_trouvs', 'Peut voir tous les trouvs du produit')
        ]

    def __str__(self):
        return self.nom


class AccesProduit(models.Model):
    utilisateur = models.ForeignKey('utilisateurs.Utilisateur', on_delete=models.CASCADE)
    produit = models.ForeignKey('produits.Produit', on_delete=models.CASCADE)
    role = models.ForeignKey('RoleProduit', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'acces_produits'
        unique_together = ('utilisateur', 'produit')

    def __str__(self):
        return f"{self.utilisateur} a accès à {self.produit}."


class RoleProduit(models.Model):
    nom = models.CharField(max_length=150, unique=True)
    description = models.TextField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'role_produits'
        permissions = [
            ('peut_voir_trouvs', 'Peut voir tous les trouvs du produit'),
            ('peut_creer_trouvs', 'Peut créer des les trouvs pour le produit'),
            ('peut_modifier_trouvs', 'Peut modifier les trouvs du produit'),
            ('peut_supprimer_trouvs', 'Peut supprimer les trouvs du produit'),
            ('peut_voir_produit', 'Peut voir le produit'),
            ('peut_creer_produit', 'Peut créer le produit'),
            ('peut_modifier_produit', 'Peut modifier le produit'),
            ('peut_supprimer_produit', 'Peut supprimer le produit'),
        ]

    def __str__(self):
        return self.nom
