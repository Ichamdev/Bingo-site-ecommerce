from django.shortcuts import render ,redirect
from django.contrib.auth import get_user_model , login , logout , authenticate
from django.contrib import messages
# Create your views here.
User = get_user_model()
def signup(request):
    if request.method =='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username,email=email,password=password)
        login(request,user)
        return redirect('index')

    return render(request,'Form/form.html')


def logout_user(request):
    logout(request)
    return redirect('index')


def login_user(request):
    if request.method == 'POST':
         username = request.POST.get('username')
         password = request.POST.get('password')
         user = authenticate(username = username , password = password)
         if user:
            login(request,user)
            return redirect('index')
         else:
             messages.info(request,'Identifiant et mot de passe incorrect')

    return render(request,'Form/login.html')





