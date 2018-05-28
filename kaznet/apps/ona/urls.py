"""
Ona App URL Configurations
"""
from rest_framework import routers
from kaznet.apps.ona.viewsets import XFormViewSet

# pylint: disable=invalid-name
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'xforms', XFormViewSet)

urlpatterns = router.urls
