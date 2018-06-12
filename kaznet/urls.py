"""
Kaznet URL Configuration
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from kaznet.apps.main.viewsets import (BountyViewSet, ClientViewSet,
                                       KaznetLocationViewSet,
                                       KaznetSubmissionsViewSet,
                                       KaznetTaskOccurrenceViewSet,
                                       KaznetTaskViewSet)
from kaznet.apps.ona.viewsets import XFormViewSet
from kaznet.apps.users.viewsets import UserProfileViewSet

ROUTER = routers.SimpleRouter()

# users
ROUTER.register(r'userprofiles', UserProfileViewSet)

# ona
ROUTER.register(r'forms', XFormViewSet)

# tasking
ROUTER.register(r'bounties', BountyViewSet)
ROUTER.register(r'clients', ClientViewSet)
ROUTER.register(r'locations', KaznetLocationViewSet)
ROUTER.register(r'submissions', KaznetSubmissionsViewSet)
ROUTER.register(r'occurrences', KaznetTaskOccurrenceViewSet)
ROUTER.register(r'tasks', KaznetTaskViewSet)

# pylint: disable=invalid-name
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/v1/', include((ROUTER.urls, 'app_name'))),
]

if settings.DEBUG:
    import debug_toolbar  # noqa
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
