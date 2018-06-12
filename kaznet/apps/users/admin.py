"""
URL Confs for users admin
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from kaznet.apps.users.models import UserProfile

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton


class UserProfileInline(admin.StackedInline):
    """
    Admin Definition for UserProfileInline
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profiles'


# Define a new User admin
# pylint: disable=function-redefined
class UserAdmin(UserAdmin):
    """
    New Definition for User Admin
    """
    inlines = (UserProfileInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
