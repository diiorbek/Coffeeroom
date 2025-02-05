from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

class UserAdmin(BaseUserAdmin):
    model = User

    list_display = ('phone_number', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'gender')

    search_fields = ('phone_number', 'first_name', 'last_name')

    ordering = ('phone_number',)

    fieldsets = (
        ('General', {'fields': ('phone_number', 'password')}),
        (_('Персональные данные'), {'fields': ('first_name', 'last_name', 'birth_date', 'gender')}),
        (_('Разрешения'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Нужные даты'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active'),
        }),
    )

    change_password_form = BaseUserAdmin.change_password_form


admin.site.register(User, UserAdmin)