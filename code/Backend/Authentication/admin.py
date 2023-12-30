from django.contrib import admin
from .forms import UserAdminCreationForm,UserAdminChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

User = get_user_model()

admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm 
    add_form = UserAdminCreationForm 
    
    list_display = ['email','username', 'admin','staff','active']
    list_filter = ['admin','staff','active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username','custom_name','description','is_verified','verify_code')}),
        ('Permissions', {'fields': ('active','staff','admin')}),
        ('Following', {'fields': ('following',), 'classes': ('wide',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','username' ,'password', 'password_2',)}
        ),
    )
    search_fields = ['email','username']
    ordering = ['email']
    filter_horizontal = ('following',)
    
    
admin.site.register(User, UserAdmin)