from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from kaznet.apps.auth_ona.provider import OnadataProvider

urlpatterns = default_urlpatterns(OnadataProvider)