from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import CustomUser, Profile


class CustomUserCreationForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Enter email'}),
        error_messages={
            'required': 'Please enter your email.',
            'invalid': 'Please enter a valid email address.'
        }
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Enter password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Confirm password'})
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']
        

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email address already exists.')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 3:
            raise forms.ValidationError(
                'Password must be at least 3 characters.')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return password2
