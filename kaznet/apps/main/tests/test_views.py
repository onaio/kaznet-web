"""
Test views module
"""
from django.contrib.auth.models import AnonymousUser
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import RequestFactory
from django.urls import reverse

from model_mommy import mommy

from kaznet.apps.main.views import ContributorNotAllowed, ReactAppView
from kaznet.apps.users.models import UserProfile


class TestViews(StaticLiveServerTestCase):
    """
    Test Views
    """

    def setUp(self):
        self.factory = RequestFactory()

    def test_react_app_view_renders(self):
        """
        Test that the ReactAppView view renders as expected
        """
        with self.settings(
            STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage'  # noqa
        ):
            request = self.factory.get(reverse('react_app'))
            request.user = mommy.make('auth.User')
            request.user.userprofile.role = UserProfile.ADMIN
            request.user.userprofile.save()

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

    def test_contributor_not_allowed_view_renders(self):
        """
        Test that the ContributorNotAllowed view renders as expected
        """
        with self.settings(
            STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage'  # noqa
        ):
            request = self.factory.get(reverse('disallow_contributors'))
            request.user = mommy.make('auth.User')
            response = ContributorNotAllowed.as_view()(request)
            self.assertEqual(response.status_code, 200)
            response.render()
            # check that the react assets are in the HTML rendered
            self.assertContains(
                response,
                'We are sorry, but only admins are allwed to access this website at this time.'  # noqa
            )
            self.assertContains(
                response,
                'Please contact an admin if you have any questions.'
            )
            self.assertContains(
                response,
                'Only Admins Can Access This Website'
            )

    def test_react_app_view_requires_authentication(self):
        """
        Test that the ReactAppView view requires authentication
        """
        request = self.factory.get(reverse('react_app'))
        request.user = AnonymousUser()
        response = ReactAppView.as_view()(request)
        # you are redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/accounts/login/?next=/', response.url)

    def test_react_app_view_contributor_access(self):
        """
        Test that the ReactAppView does not allow contributor access
        """
        request = self.factory.get(reverse('react_app'))
        request.user = mommy.make('auth.User')
        request.user.userprofile.role = UserProfile.CONTRIBUTOR
        request.user.userprofile.save()
        response = ReactAppView.as_view()(request)
        # you are redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/contributors', response.url)

    def test_contributor_not_allowed_view_requires_authentication(self):
        """
        Test that the ContributorNotAllowed view requires authentication
        """
        request = self.factory.get(reverse('disallow_contributors'))
        request.user = AnonymousUser()
        response = ContributorNotAllowed.as_view()(request)
        # you are redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/accounts/login/?next=/contributors', response.url)
