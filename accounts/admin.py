from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin # to make password uneditable at the admin site

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "username","last_login","date_joined", "is_active")
    list_display_links = ("email", "first_name", "last_name") # using these fields, you will be able to get inside of the data
    readonly_fields = ("last_login","date_joined")  # you won't be able to get inside o these fields
    ordering = ("-date_joined", ) # to make it tuple , due to single vlaue. if multiple fields are there, it will show in desc order due to -
    
    # to make password readonly
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)