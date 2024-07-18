from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    custom_user_list = ('surname', 'name', 'patronymic', 'gender', 'birth_date', 'created', 'updated')
    list_display = UserAdmin.list_display + custom_user_list

    readonly_fields = ['created', 'updated']

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': custom_user_list}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': custom_user_list}),
    )

admin.site.register(User, CustomUserAdmin)