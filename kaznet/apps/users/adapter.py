"""
Custom AllAuth adapter module

https://github.com/pennersr/django-allauth
"""
from django.contrib.auth.models import User

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom social account adapter
    """

    # pylint: disable=unused-argument
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed
        (and before the pre_social_login signal is emitted).

        We're trying to solve different use cases:
        - social account already exists, just go on
        - social account has no email or email is unknown, just go on
        - social account has no username or username is unknown, just go on
        - social account's email exists, link to existing user
        - social account's username exists, link to existing user

        Credits: https://stackoverflow.com/a/30591838
        """

        # Ignore existing social accounts, just do this stuff for new ones
        if not sociallogin.is_existing:
            # let us start with checking for an existing user by username
            username = sociallogin.account.extra_data.get('username')

            if username is not None:
                try:
                    # check if the given username exists
                    user = User.objects.get(username=username.lower())
                except User.DoesNotExist:  # pylint: disable=no-member
                    # if it does not, let allauth take care of this new
                    # social account
                    pass
                else:
                    # if it does, connect this new social login to the
                    # existing user
                    return sociallogin.connect(request, user)

            # next we check for an existing user by email
            email = sociallogin.account.extra_data.get('email')

            if email is not None:
                # check if given email address already exists.
                # Note: __iexact is used to ignore cases
                try:
                    email_address = EmailAddress.objects.get(
                        email__iexact=email.lower())
                except EmailAddress.DoesNotExist:  # pylint: disable=no-member
                    # if it does not, let allauth take care of this new
                    # social account
                    pass
                else:
                    # if it does, connect this new social login to the
                    # existing user
                    user = email_address.user
                    return sociallogin.connect(request, user)

        # in all other cases, just let allauth do its regular thing
        return None


class AccountAdapter(DefaultAccountAdapter):
    """
    Custom Account Adapter
    """

    def is_open_for_signup(self, request):  # pylint: disable=unused-argument
        """
        Don't allow signups
        """
        return True
