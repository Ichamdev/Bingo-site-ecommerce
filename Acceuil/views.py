from urllib import request
from django.shortcuts import render , get_object_or_404 ,redirect
from django.urls import reverse
from .models import Categories , Products , Cart, Order

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
import uuid
import requests
from .form import Creat_order, LivraisonForm,ContactForm

# Create your views here.

def index(request):
    categorie = Categories.objects.all()
    produit = Products.objects.all()
    return render(request,'index.html',context={'categorie':categorie,'products':produit})


def detail(request,name):
    produit = get_object_or_404(Products,name = name)
    categorie = Categories.objects.all()
    return render(request,'detail.html',context={'product':produit,'categorie':categorie})


def categori(request,id):
    produit = Products.objects.filter(categorie_id=id)
    categorie = Categories.objects.all()
    return render(request,'categorie.html',context={'products':produit,'categorie':categorie})


def rechercher (request):
    if request.method == 'POST':
        search = request.POST.get('rechercher')
        produit = Products.objects.filter(name__icontains=search)
        categorie = Categories.objects.all()
        return render(request,'index.html',context={'products':produit,'categorie':categorie})
    else:
        return redirect('index')


# def users(request):
#    if request.user.is_authenticated:
#     produit = Products.objects.filter(user=request.user)
#     return render(request,'profil.html',context={'products':produit})
#    else:
#       return redirect('login_user')
   


def cart(request):
    cart = get_object_or_404(Cart , user = request.user)
    categorie = Categories.objects.all()
    return render(request,'cart.html',context={"orders":cart.orders.all() ,"categorie":categorie })

def add_to_card(request,name):
    user = request.user
    product = get_object_or_404(Products,name=name)
    cart, _ = Cart.objects.get_or_create(user=user)
    if not user:
        return redirect('login_user')
    order , created =Order.objects.get_or_create(user=user,ordered = False , product=product)
    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity+=1
        order.save()
    # return redirect(reverse("detail", kwargs={'name':name}))
    return redirect('cart')




def updatecart(request,id):
    cart = Cart.objects.get(user=request.user)
    produit = Order.objects.get(id=id, user=request.user)
    if request.method == 'POST':
        form = Creat_order(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('cart')



def delete_cart(request,id):
    cart = Cart.objects.get(user=request.user)
    produit = Order.objects.get(id=id, user=request.user)
    produit.delete()
    cart.save()

    return redirect('index')




def livraison_view(request):
    categorie = Categories.objects.all()
    if request.method == 'POST':
        form = LivraisonForm(request.POST)
        cart = Cart.objects.get(user=request.user)

        if form.is_valid():
            livraison = form.save()

            # Contenu de l’email
            sujet = "Nouvelle commande de livraison"
            message = f"""
            Nouvelle commande :

            Nom: {livraison.nom}
            Adresse: {livraison.adresse}
            Ville: {livraison.ville}
            Téléphone: {livraison.telephone}
            Produits commandés:
            {''.join(f"""
                    Nom du produit: {order.product.name} (Quantité: {order.quantity})""" for order in cart.orders.all())}
            """

            # Envoi de l’email
           
            send_mail(
                    sujet,
                    message,
                    settings.EMAIL_HOST_USER,
                    ['salouakanho@gmail.com'],  # Change ceci
                    fail_silently=True,
                )

            messages.info(request,'Votre commande a été reçue avec succès. Nous vous contacterons dans quelque minute')
            cart.orders.all().delete()
            cart.save()
            return redirect('index')
          
               
    else:
        form = LivraisonForm()

    return render(request, 'Livraison.html', {'form': form , 'categorie':categorie} )


def quisomme_nous(request):
    return render(request, 'quisommesnous.html')


def conditions_generales(request):
    return render(request, 'conditions_generales.html')


def termes(request):
    return render(request, 'Termes.html')


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Sauvegarde dans la base
            message_contact = form.save()

            # Préparation du contenu de l'email
            contenu = (
                f"Nom : {message_contact.nom}\n"
                f"Email : {message_contact.email}\n\n"
                f"Message :\n{message_contact.message}"
            )

            # Envoi d'email
            send_mail(
                message_contact.sujet,
                contenu,
                settings.DEFAULT_FROM_EMAIL,
                ['ichamsalou@gmail.com'],  # Remplace par ton email
                fail_silently=True
            )

            messages.success(request, 'Votre message a été envoyé avec succès.')
            return redirect('contact')


    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def contact_success(request):
    return render(request, 'success.html')




# def paiement_view(request):
#     url = "https://api-checkout.cinetpay.com/v2/payment"
    
    
#     if Cart:
#         cart = Cart.objects.get(user=request.user)
#         total_amount = sum(order.product.price * order.quantity for order in cart.orders.all())
#     headers = {
#         "Content-Type": "application/json"
#     }

#     data = {
#         "amount": str(total_amount),  # Montant total de la commande
#         "currency": "XOF",
#         "apikey": settings.CINETPAY_API_KEY,
#         "site_id": settings.CINETPAY_SITE_ID,
#         "transaction_id": str(uuid.uuid4()),  # à générer dynamiquement
#         "description": "Paiement du produit",
#         "customer_name": "Client",
#         "customer_surname": "Nom",
#         "customer_email": str(request.user.email),
#         "notify_url": "http://127.0.0.1:8000/cinetpay/notify/",
#         "return_url": "http://127.0.0.1:8000/cinetpay/success/"
#     }

#     response = requests.post(url, headers=headers, json=data)
#     res = response.json()

#     if "data" in res and "payment_url" in res["data"]:
#         print("Redirection vers l'URL de paiement")
#         return redirect(res["data"]["payment_url"])
#     else:
#         return HttpResponse("Erreur lors de l'initiation du paiement")


# def notify(request):
#         # Traitez la notification de paiement ici
#         return HttpResponse("Notification reçue avec succès")


# def success(request):
#         # Traitez la réussite du paiement ici
#         return HttpResponse("Paiement réussi")
