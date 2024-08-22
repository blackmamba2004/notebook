from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

from django.utils.translation import gettext_lazy as _

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password',)}),
        (
            _('Personal info'), 
            {
                'fields': (
                    'first_name', 
                    'last_name', 
                    'email',
                    'gender', 
                    'birth_date',
                )
            }
        ),
        (
            _('Permissions'), 
            {
                'fields': (
                    'is_active', 
                    'is_staff', 
                    'is_superuser', 
                    'groups', 
                    'user_permissions',
                )
            }
        ),
        (_('About account'), {'fields': ('created', 'updated',)}),
        # (_('Important dates'), {'fields': ('date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active',)}
        ),
    )
    
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups',)
    search_fields = ('username', 'email', 'first_name', 'last_name',)
    ordering = ('email', 'username',)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    readonly_fields = ['created', 'updated']

admin.site.register(User, CustomUserAdmin)
