"""
Kaznet URL Configuration
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path

from rest_framework import routers
from kaznet.apps.main.views import ReactAppView, ContributorNotAllowed
from kaznet.apps.main.viewsets import (BountyViewSet, ClientViewSet,
                                       ContentTypeViewSet,
                                       KaznetLocationTypeViewSet,
                                       KaznetLocationViewSet,
                                       KaznetSubmissionsViewSet,
                                       KaznetTaskOccurrenceViewSet,
                                       KaznetTaskViewSet,
                                       SubmissionExportViewSet)
from kaznet.apps.ona.views import create_or_update_instance
from kaznet.apps.ona.viewsets import XFormViewSet
from kaznet.apps.users.viewsets import UserProfileViewSet

ROUTER = routers.SimpleRouter()

# users
ROUTER.register(r'userprofiles', UserProfileViewSet)

# ona
ROUTER.register(r'forms', XFormViewSet)

# main
ROUTER.register(r'bounties', BountyViewSet)
ROUTER.register(r'clients', ClientViewSet)
ROUTER.register(r'locations', KaznetLocationViewSet)
ROUTER.register(r'locationtypes', KaznetLocationTypeViewSet)
ROUTER.register(r'submissions', KaznetSubmissionsViewSet)
ROUTER.register(r'exports/submissions', SubmissionExportViewSet)
ROUTER.register(r'occurrences', KaznetTaskOccurrenceViewSet)
ROUTER.register(r'tasks', KaznetTaskViewSet)
ROUTER.register(r'contenttypes', ContentTypeViewSet)

# pylint: disable=invalid-name
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/v1/', include((ROUTER.urls, 'app_name'))),

    # no contributors
    path(
        'contributors',
        ContributorNotAllowed.as_view(),
        name="disallow_contributors"
    ),

    path('webhook/', create_or_update_instance, name="webhook"),

    # react view to handle all other matches
    re_path(r'^$', ReactAppView.as_view(), name="react_app"),
    re_path(r'^(?:.*)/$', ReactAppView.as_view()),
]

if settings.DEBUG:
    try:
        import debug_toolbar  # noqa pylint: disable=E0401
    except ModuleNotFoundError:
        pass
    else:
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
