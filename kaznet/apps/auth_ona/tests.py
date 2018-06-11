from allauth.socialaccount.tests import create_oauth2_tests
from allauth.tests import MockedResponse
from allauth.socialaccount.providers import registry

from kaznet.apps.auth_ona.provider import OnadataProvider


class OnadataTests(create_oauth2_tests(registry.by_id(OnadataProvider.id))):
    def get_mocked_response(self):
        return MockedResponse(200, """
        {
            "expires_at": "2012-03-22T16:56:48-05:00",
            "identity": {
                "id": 9999999,
                "first_name": "Jason Fried",
                "last_name": "Jason Fried",
                "email_address": "jason@example.com"
            },
            "accounts": [
                {
                    "product": "bcx",
                    "id": 88888888,
                    "name": "Wayne Enterprises, Ltd.",
                    "href": "https://example.com/88888888/api/v1"
                },
                {
                    "product": "bcx",
                    "id": 77777777,
                    "name": "Veidt, Inc",
                    "href": "https://example.com/77777777/api/v1"
                },
                {
                    "product": "campfire",
                    "id": 44444444,
                    "name": "Acme Shipping Co.",
                    "href": "https://acme4444444.campfirenow.com"
                }
            ]
        }""")