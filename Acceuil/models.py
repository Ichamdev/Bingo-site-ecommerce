from django.db import models
from django.urls import reverse
from django.utils import timezone
from Bingo.settings import AUTH_USER_MODEL

class Categories(models.Model):
    name =models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name
    

class Products(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    categorie = models.ForeignKey(Categories,on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='products', blank=True, null=True)

    def __str__(self):
        return self.name
    

class Order(models.Model): # represente les produits
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True,null=True)
    
    
    def __str__(self):
        return f"{self.product.name} ({self.quantity}) "
    


class Cart(models.Model): # represente les panier de produit
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
 
    def __str__(self):
        return self.user.username



class Livraison(models.Model):
    nom = models.CharField(max_length=200)
    adresse = models.CharField(max_length=200)
    ville = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.ville}"

    


    # def delete(self,*args,**kwargs):
    #     self.orders.clear()
    #     super().delete(*args,**kwargs)



class MessageContact(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    sujet = models.CharField(max_length=150)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.sujet}"

    
    