"""
Custom AllAuth adapter module

https://github.com/pennersr/django-allauth
"""
from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    """
    Custom Account Adapter
    """

    def is_open_for_signup(self, request):  # pylint: disable=unused-argument
        """
        Don't allow signups
        """
        return True
