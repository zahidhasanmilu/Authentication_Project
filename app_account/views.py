from django.shortcuts import render,HttpResponse
from .forms import CustomUserCreationForm

# Create your views here.


def user_signup(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('User Created Successfully')
    context = {'form': form}
    return render(request, 'app_account/user_signup.html',context)