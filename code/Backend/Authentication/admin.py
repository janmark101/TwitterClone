from django.contrib import admin
from .forms import UserAdminCreationForm,UserAdminChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

User = get_user_model()

admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm #change form in admin will be ours from useradminchangeform
    add_form = UserAdminCreationForm #admin change form in admin will be ours from useradmincreationform
    
    list_display = ['email', 'admin','staff','active']
    list_filter = ['admin','staff','active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username','description')}),
        ('Permissions', {'fields': ('active','staff','admin')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_2',)}
        ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()
    
    
admin.site.register(User, UserAdmin)