
from django.urls import path
from .views import signup , logout_user , login_user

urlpatterns = [
    path('',login_user,name='login_user'),
    path('register/',signup,name='signup'),
    path('logout_user/',logout_user,name='logout_user'),
]
