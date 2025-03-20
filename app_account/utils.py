from django.shortcuts import redirect, HttpResponse
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail

def logout_required(view_func):
    """
    Custom decorator to restrict access to logged-in users.
    Redirects logged-in users to a specific page.
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse('You are already logged in.')
        return view_func(request, *args, **kwargs)
    return wrapper



#####----------------------------------------------------------------

def send_verification_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(str(user.pk).encode('utf-8'))
    domain = get_current_site(request).domain
    link = f'http://{domain}/verify-email/{uid}/{token}/'

    subject = 'Verify Your Email'
    message = render_to_string('app_account/verification_email.html', {
        'user': user,
        'link': link,
    })

    send_mail(subject, message, 'noreply@example.com', [user.email])

def send_password_reset_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    current_site = get_current_site(request)

    verification_link = (
        f"http://{current_site.domain}/accounts/reset-password/{uid}/{token}"
    )

    email_subject = "Reset Your Password"
    email_body = render_to_string(
        "app_account/verification_email.html",
        {"user": user, "verification_link": verification_link},
    )

    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )

    email.content_subtype = "html"
    email.send()