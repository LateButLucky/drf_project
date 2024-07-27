from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'phone', 'city', 'avatar'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password', 'phone', 'city', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    list_display = ('email', 'phone', 'city', 'is_staff')
    search_fields = ('email', 'phone', 'city')
    ordering = ('email',)


admin.site.register(User, UserAdmin)
