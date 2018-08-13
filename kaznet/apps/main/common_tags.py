"""
Main Common tags
"""
from django.utils.translation import ugettext_lazy as _


INCORRECT_CLONE_DATA = _('Incorrect data.')
SAME_PARENT = _('An object cannot be its own parent.')
INCORRECT_LOCATION = _('Submitted from wrong location')
LACKING_EXPERTISE = _('User Expertise level does not meet Requirement')
INVALID_SUBMISSION_TIME = _('Data Submitted at wrong time.')
INVALID_TASK = _('Can not submit data to invalid Task.')
MISSING_START_DATE = _('Cannot determine the start date.  Please provide '
                       'either the start date or timing rule(s)')
AUTH_USER_DOESNT_EXIST = _('Invalid User. User does not exist.')
AUTH_USER_NOT_LOGGED_IN = _('User not logged into Ona.')
INVALID_TOKEN_CREDENTIALS_MISSING = _('Invalid token header. No credentials'
                                      ' provided.')
INVALID_TOKEN_SPACES_CONTAINED = _('Invalid token header. Token string should'
                                   ' not contain spaces')
PAST_END_DATE = _(
    'Cannot create an active task with an end date from the past.')
