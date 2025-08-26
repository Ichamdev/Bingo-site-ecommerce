from django import forms
from .models import Products , Order , Livraison 

class Creat_order(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['quantity']
        labels = {
            'quantity':'Quantite commandez',
                }




class LivraisonForm(forms.ModelForm):
    class Meta:
        model = Livraison
        fields = ['nom','adresse', 'ville',  'telephone']



from django import forms
from .models import MessageContact

class ContactForm(forms.ModelForm):
    class Meta:
        model = MessageContact
        fields = ['nom', 'email', 'sujet', 'message']
        labels = {
            'nom': 'Nom',
            'email': 'Email',
            'sujet': 'Sujet',
            'message': 'Message',
        }
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }


        

    
