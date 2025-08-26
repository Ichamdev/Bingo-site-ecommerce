from django.contrib import admin
from .models import Categories , Products , Order , Cart ,Livraison
# Register your models here.

admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Livraison)