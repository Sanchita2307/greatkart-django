from django.contrib import admin
from .models import Account, UserProfile
from django.contrib.auth.admin import UserAdmin # to make password uneditable at the admin site
from django.utils.html import format_html

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

# class UserProfileAdmin(admin.ModelAdmin):
#     def thumbnail(self, object):
#         return format_html(
#             '<img src="{}" width="30" style="border-radius:50%;">',
#             object.profile_picture.url
#         )   
#     list_display = ('thumbnail', 'user', 'city', 'state', 'country')         
class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="30" style="border-radius:50%;">',
                obj.profile_picture.url
            )
        return "No Image"  # fallback text or you can show a placeholder image

    thumbnail.short_description = "Profile Picture"

    list_display = ('thumbnail', 'user', 'city', 'state', 'country')  


admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)