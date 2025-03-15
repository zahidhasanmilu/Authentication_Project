from django.shortcuts import render,HttpResponse
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from app_account.utils import logout_required

# Create your views here.

@logout_required
def user_signup(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('User Created Successfully')
    context = {'form': form}
    return render(request, 'app_account/user_signup.html',context)



@logout_required
def user_login(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password,  backend='app_account.authentication_backends.EmailBackEnd')  

        if user is not None:
            login(request, user)
            messages.success(request, "User Logged In Successfully!")
            return HttpResponse('User login Successfully')
        else:
            return HttpResponse('Invalid Credentials! Please try again.')   
         
    return render(request, 'app_account/user_login.html')