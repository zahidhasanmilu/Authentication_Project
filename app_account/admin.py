from django.contrib import admin
from . models import CustomUser, Profile


class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ['email', 'first_name',
                    'is_staff', 'is_active', 'is_superuser']
    search_fields = ['email', 'username']
    list_filter = ['is_staff', 'is_active', 'is_superuser']
    ordering = ['-date_joined']


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['user',  'full_name',
                    'address_line_1', 'city', 'state', 'country', 'user__is_verified']
    search_fields = ['user__email', 'city', 'state', 'country']
    list_filter = ['city', 'state', 'country']
    ordering = ['user__email']


# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
