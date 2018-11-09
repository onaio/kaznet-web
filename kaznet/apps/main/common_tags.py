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
SUBMISSIONS_MORE_THAN_LIMIT = _('User Submissions for this task more than '
                                'the set limit per user')
AUTH_USER_DOESNT_EXIST = _('Invalid User. User does not exist.')
INVALID_TOKEN_CREDENTIALS_MISSING = _('Invalid token header. No credentials'
                                      ' provided.')
INVALID_TOKEN_SPACES_CONTAINED = _('Invalid token header. Token string should'
                                   ' not contain spaces')
PAST_END_DATE = _(
    'Cannot create an active task with an end date from the past.')

LABEL_USER = _('User')
LABEL_USER_ID = _('User Id')
LABEL_TASK = _('Task')
LABEL_TASK_ID = _('Task Id')
LABEL_LOCATION = _('Location')
LABEL_LOCATION_ID = _('Location Id')
LABEL_SUBMISSION_TIME = _('Submission Time')
LABEL_AMOUNT = _('Amount')
LABEL_CURRENCY = _('Currency')
LABEL_PHONE = _('Phone Number')
LABEL_PAYMENT_PHONE = _('Payment Phone Number')
LABEL_STATUS = _('Status')
KAZNET_WEBHOOK_NAME = 'generic_json'

HAS_WEBHOOK_FIELD_NAME = 'has_webhook'
WEBHOOK_FIELD_NAME = 'webhooks'
HAS_FILTERED_DATASETS_FIELD_NAME = 'has_filtered_data_sets'
FILTERED_DATASETS_FIELD_NAME = 'filtered_datasets'
