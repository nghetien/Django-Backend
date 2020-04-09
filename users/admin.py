from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.


class UserAdmin(UserAdmin):
    list_display = ('email','username','date_joined',
                    'last_login','is_admin','is_staff','phone','company')
    search_fields = ('email','username',)
    readonly_fields = ('date_joined','last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User,UserAdmin)