from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import F


class Customer(models.Model):
     STATUT = (
            ('actif', 'Actif'),
            ('inactif', 'Inactif'),
        )

     nom_complet = models.CharField(max_length=200, null=True)
     telephone = models.CharField(max_length=16, null=True, unique=True)
     email = models.EmailField(null=True, unique=True) 
     date_de_naissance = models.DateField(null=True, blank=True)
     adresse = models.CharField(max_length=255, null=True, blank=True)
     total_des_depenses = models.PositiveIntegerField(default=0, null=True)
     date_enregistrement = models.DateTimeField(auto_now_add=True)
     statut = models.CharField(max_length=7, choices=STATUT, default='actif')

     def __str__(self):
          return self.nom_complet

     # def get_absolute_url(self):
     #    return reverse('management:home')


class Brand(models.Model):
     code = models.CharField(max_length=50, null=True)
     nom = models.CharField(max_length=50, null=True)

     def __str__(self):
          return self.nom 
          
          
class Category(models.Model):
     code = models.CharField(max_length=50, null=True)
     nom = models.CharField(max_length=50, null=True,)

     def __str__(self):
          return self.nom

class Stock(models.Model):
     code = models.CharField(max_length=50, null=True, unique=True)
     quantite = models.PositiveIntegerField(null=True, default = 0)
     prix = models.PositiveIntegerField(null=True, default=0)
     remise = models.PositiveIntegerField(default=0, blank=True, null=True)
     prix_final = models.PositiveIntegerField(default=0, null=True, blank=True)
     description = models.CharField(max_length=200, null=True, blank=True)
     date_enregistrement = models.DateTimeField(auto_now_add=True)
     categorie = models.ForeignKey('Category', null=True, on_delete=models.CASCADE)
     marque = models.ForeignKey('Brand', null=True, on_delete=models.CASCADE)

     def __str__(self):
          return self.code


class Product(models.Model):
     SIZE = (
               ('XS', 'XS'),
               ('S', 'S'),
               ('M', 'M'),
               ('L', 'L'),
               ('XL', 'XL'),
               ('XXL', 'XXL'),
          )
          
     code = models.CharField(max_length=50, null=True, unique=True)
     taille = models.CharField(max_length=6, null=True, blank=True, choices=SIZE, default='XS')
     commande = models.ForeignKey('Order', null=True, blank=True, on_delete=models.SET_NULL)
     stock = models.ForeignKey('Stock', null=True, blank=True, on_delete=models.CASCADE, default=None)
     def __str__(self):
          return self.code


class Order(models.Model):
     STATUS = (
               ('Payé', 'Payé'),
               ('Impayé', 'Impayé'),
          )

     client = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
     date_enregistrement = models.DateTimeField(auto_now_add=True, null=True)
     total_pcs = models.PositiveIntegerField(default=0, blank=True, null=True)
     montant_total = models.PositiveIntegerField(default=0.0, blank=True, null=True)
     remise = models.PositiveIntegerField(default=0, blank=True, null=True)
     somme_finale = models.PositiveIntegerField(default=0.0, blank=True, null=True)
     statut = models.CharField(max_length=8, null=True, blank=True, choices=STATUS, default='Payé')
     note = models.CharField(max_length=255, null=True, blank=True)
     
     def __str__(self):
          return str(self.pk) + ' - ' + self.client.nom_complet
