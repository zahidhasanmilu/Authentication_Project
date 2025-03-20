from django.shortcuts import redirect, render, HttpResponse

from app_account.authentication_backends import EmailBackEnd
from app_account.models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from app_account.utils import logout_required
from django.contrib.auth import update_session_auth_hash
from app_account.utils import send_password_reset_email, send_verification_email





def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = get_user_model().objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_verified = True
            user.save()
            messages.success(request, "Your email has been verified!")
            return redirect('user_login')  # Redirect to login page
        else:
            messages.error(request, "Invalid verification link!")
            # Redirect to login page in case of failure
            return redirect('user_login')
    except get_user_model().DoesNotExist:
        messages.error(request, "User not found!")
        # Redirect to login page if user is not found
        return redirect('user_login')
    except Exception as e:
        messages.error(request, f"Error: {e}")
        # Redirect to login page in case of error
        return redirect('user_login')


@logout_required
def user_signup(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_verified = False  # Initially, is_verified is set to False            
            # Manually hash the password before saving the user
            user.set_password(form.cleaned_data['password1'])  # Hash the password
            user.save()
            # Send email verification link
            send_verification_email(user, request)

            messages.success(request, "User Created Successfully! Please verify your email.")
            return redirect('user_login')
    context = {'form': form}
    return render(request, 'app_account/user_signup.html', context)




@logout_required
def user_login(request):
    # If user is already authenticated, check if the email is verified

        
    # If the request method is POST, handle login form submission
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user using the custom email backend
        user = authenticate(request, email=email, password=password, backend=EmailBackEnd)
        if user.is_verified==False:
            messages.error(request, "Please verify your email first.")
            return redirect('user_login')
        if user is not None and user.is_verified==True:
            login(request, user)
            messages.success(request, "User Logged In Successfully!")
            return redirect('home')  # Redirect to the home or dashboard page
        else:
            # If authentication fails, display an error message
            messages.error(request, "Invalid email or password!")
            return redirect('user_login')  # Redirect back to login page for retry

    return render(request, 'app_account/user_login.html')



def user_logout(request):
    logout(request)
    return redirect('user_login')  # Redirect to the login page after logout

from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

def password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user_model = get_user_model()

        try:
            user = user_model.objects.get(email=email)
        except user_model.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return redirect("password_reset")

        send_password_reset_email(request, user)
        messages.info(request, "Password reset instructions have been sent to your email.")
        return redirect("user_login")

    return render(request, "app_account/forgot.html")


def set_new_password(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to change your password.")
        return redirect("user_login")

    if request.method == "POST":
        password = request.POST.get("password")

        try:
            validate_password(password, request.user)
            request.user.set_password(password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Your password has been updated successfully.")
            return redirect("home")
        except ValidationError as e:
            messages.error(request, e.messages[0])

    return render(request, "app_account/new-password.html")


def custom_password_reset(request, uidb64, token):
    if request.method == "POST":
        password1 = request.POST.get("new_password1")
        password2 = request.POST.get("new_password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect(request.path)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)

            if not default_token_generator.check_token(user, token):
                messages.error(request, "Invalid or expired token!")
                return redirect("password_reset")

            validate_password(password1, user)  # Django's built-in password validation
            user.set_password(password1)
            user.save()
            update_session_auth_hash(request, user)

            messages.success(request, "Password has been reset successfully!")
            return redirect("user_login")

        except (ValueError, get_user_model().DoesNotExist):
            messages.error(request, "Invalid reset link. Please request a new one.")
            return redirect("password_reset")

    return render(request, "app_account/password_reset_confirm.html")