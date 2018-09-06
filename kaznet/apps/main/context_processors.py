"""
Context processors module
"""
from django.conf import settings


def kaznet_processor(request):
    """
    Sets useful template variables
    """
    return {
        'ONA_BASE_URL': settings.ONA_BASE_URL
    }
