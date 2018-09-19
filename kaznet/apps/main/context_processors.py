"""
Context processors module
"""
from django.conf import settings
from django.utils.translation import ugettext as _


def kaznet_processor(request):  # pylint: disable=unused-argument
    """
    Sets useful template variables
    """
    return {
        'ONA_BASE_URL': settings.ONA_BASE_URL,
        'ONA_LOGIN_TEXT': _(settings.ONA_LOGIN_TEXT)
    }
