"""
Test views module
"""
from django.contrib.auth.models import AnonymousUser
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import RequestFactory
from django.urls import reverse

from model_mommy import mommy

from kaznet.apps.main.views import ReactAppView


class TestReactAppView(StaticLiveServerTestCase):
    """
    Test ReactAppView
    """

    def setUp(self):
        self.factory = RequestFactory()

    def test_view_renders(self):
        """
        Test that the view renders as expected
        """
        with self.settings(
            STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage'  # noqa
        ):
            request = self.factory.get(reverse('react_app'))
            request.user = mommy.make('auth.User')
            response = ReactAppView.as_view()(request)
            self.assertEqual(response.status_code, 200)
            response.render()
            # check that the react assets are in the HTML rendered
            self.assertContains(
                response,
                '<link rel="shortcut icon" href="/static/react/favicon.ico">'
            )
            self.assertContains(
                response,
                '<link rel="manifest" href="/static/react/manifest.json">'
            )
            self.assertContains(
                response,
                '<link href="/static/react/css/main.css" rel="stylesheet">'
            )
            self.assertContains(
                response,
                '<script type="text/javascript" src="/static/react/js/main.js"></script>'  # noqa
            )
            self.assertContains(
                response,
                '<div id="kaznet-root" class="kaznet-root"></div>'
            )

    def test_requires_authentication(self):
        """
        Test that the view requires authentication
        """
        request = self.factory.get(reverse('react_app'))
        request.user = AnonymousUser()
        response = ReactAppView.as_view()(request)
        # you are redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/accounts/login/?next=/', response.url)
