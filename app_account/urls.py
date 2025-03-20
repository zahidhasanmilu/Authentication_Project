from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('signup/', views.user_signup, name='user_signup'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('password-reset/',views.password_reset, name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="app_account/password_reset_done.html"), name='password_reset_done'),
    path('reset-password/<uidb64>/<token>/', views.custom_password_reset, name="password_reset_confirm"),
    path("set-new-password/", views.set_new_password, name="new-password"),

]
