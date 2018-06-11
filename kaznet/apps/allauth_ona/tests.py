"""
Tests module for allauth_ona
"""
from allauth.socialaccount.tests import OAuth2TestsMixin
from allauth.tests import MockedResponse, TestCase

from .provider import OnadataProvider


class OnadataTests(OAuth2TestsMixin, TestCase):
    """
    Onadata provider tests
    """
    provider_id = OnadataProvider.id

    def get_mocked_response(self):
        return MockedResponse(200, """
        {
            "url": "http://127.0.0.1:9000/api/v1/profiles/tranx16",
            "username": "tranx16",
            "name": "",
            "email":
            "trx@example.com",
            "city": "",
            "country": "",
            "organization": "",
            "website": "",
            "twitter": "",
            "gravatar": "https://secure.gravatar.com/avatar/6fa9f4c9f561c6bcd2b29c430e0358ed?s=60&d=https%3A%2F%2Fona.io%2Fstatic%2Fimages%2Fdefault_avatar.png",
            "require_auth": false,
            "user": "http://127.0.0.1:9000/api/v1/users/tranx16",
            "api_token": "4c4927fdfc38198cfb8de1cc501944418472906d",
            "temp_token": "78022a82bf2852aeeba879f04b8719640d6eba6c"
        }
        """)  # noqa
