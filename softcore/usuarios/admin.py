from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser

admin.site.register(CustomUser)

"""
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['correo','is_staff', 'nombre']

admin.site.register(CustomUser, CustomUserAdmin)
"""
"""
    class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.admin
"""