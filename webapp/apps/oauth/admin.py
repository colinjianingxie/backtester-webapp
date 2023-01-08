from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from oauth.models import Account
from oauth.models import Admin
from oauth.models import User

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('id', 'email', 'username', 'date_joined', 'last_login', 'is_admin', 'account_type', 'is_staff',)   # What to display as columns in
    search_fields = ('id', 'email', 'username', 'account_type',)
    readonly_fields = ('id','date_joined', 'last_login', 'account_type')
    ordering = ('email',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        #('Permissions', {'fields': ['is_staff']}), # might need groups, user_permissions
    )

class UserAdmin(UserAdmin):
    list_display = ('id', 'account',)   # What to display as columns in
    search_fields = ('id', 'account',)
    readonly_fields = ('id', 'account',)
    ordering = ('id',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        #('Permissions', {'fields': ['is_staff']}), # might need groups, user_permissions
    )

class AdminAdmin(UserAdmin):
    list_display = ('id', 'account',)   # What to display as columns in
    search_fields = ('id', 'account',)
    readonly_fields = ('id', 'account',)
    ordering = ('id',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        #('Permissions', {'fields': ['is_staff']}), # might need groups, user_permissions
    )


admin.site.register(Account, AccountAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Admin, AdminAdmin)
