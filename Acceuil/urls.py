from django.urls import path
from .views import index , detail , categori , add_to_card, cart , delete_cart , livraison_view , updatecart ,rechercher, quisomme_nous , conditions_generales , termes, contact_view 


urlpatterns = [
    path('',index,name ='index'),
    path('rechercher/', rechercher, name='rechercher'),
    path('a propos de nous/', quisomme_nous, name='quisommesnous'),
    path('conditions_generales/', conditions_generales, name='conditions_generales'),
    path('termes/', termes, name='termes'),
    path('contact/',contact_view, name='contact'),
    path('cart/',cart,name = 'cart'),
    path('cart/update/<int:id>/',updatecart,name = 'update_cart'),
    path('cart/delete/<int:id>/',delete_cart,name = 'delete_cart'),
    path('livraison/', livraison_view, name='livraison'),
    path('<int:id>/',categori,name='categorie'),
    path('<str:name>/',detail,name='detail'),
    path('<str:name>/add_to_card/',add_to_card,name='add_to_card'),
    # path('profil',users,name='profil'),
 
]
