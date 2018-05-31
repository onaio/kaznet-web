"""
Models from Onadata

See: https://github.com/onaio/onadata
"""

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from tasking.models.base import TimeStampedModel

from kaznet.apps.ona.constants import MAX_ID_LENGTH, XFORM_TITLE_LENGTH
from kaznet.apps.ona.managers import GenericSoftDeleteManager


class XForm(TimeStampedModel, models.Model):
    """
    XForm model from onadata
    """
    ona_pk = models.PositiveIntegerField(
        _("Onadata Primary Key"), db_index=True, unique=True, blank=False)
    project_id = models.PositiveIntegerField(
        _("Project ID"), db_index=True, unique=False, blank=False)
    title = models.CharField(
        _('Title'), editable=False, max_length=XFORM_TITLE_LENGTH)
    id_string = models.SlugField(
        _('ID String'),
        editable=False,
        max_length=MAX_ID_LENGTH)
    deleted_at = models.DateTimeField(
        _('Deleted at'), null=True, default=None)
    last_updated = models.DateTimeField(
        _('Last Updated'),
        null=True,
        blank=True,
        default=None)
    objects = GenericSoftDeleteManager()

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta Options for XForm
        """
        ordering = ['title', 'id_string']
        unique_together = ('project_id', 'id_string')

    def __str__(self):
        return self.title


class Instance(TimeStampedModel, models.Model):
    """
    Instance model from onadata
    """
    ona_pk = models.PositiveIntegerField(
        _("Onadata Primary Key"), db_index=True, unique=True, blank=False)
    xform = models.ForeignKey(
        'ona.XForm', null=False, on_delete=models.PROTECT)
    json = JSONField(default=dict, null=False)
    deleted_at = models.DateTimeField(
        _('Deleted at'), null=True, default=None)
    last_updated = models.DateTimeField(
        _('Last Updated'),
        null=True,
        blank=True,
        default=None)
    objects = GenericSoftDeleteManager()

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta Options for Instance
        """
        ordering = ['ona_pk', 'deleted_at']


class Project(TimeStampedModel, models.Model):
    """
    Project model from onadata
    """
    ona_pk = models.PositiveIntegerField(
        _("Onadata Primary Key"), db_index=True, unique=True, blank=False)
    organization = models.PositiveIntegerField(
        _("Organization ID"),
        blank=True,
        null=True,
        default=None
        )
    name = models.CharField(max_length=255)
    deleted_at = models.DateTimeField(
        _('Deleted at'), null=True, default=None)
    last_updated = models.DateTimeField(
        _('Last Updated'),
        null=True,
        blank=True,
        default=None)

    objects = GenericSoftDeleteManager()

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta Options for Project
        """
        ordering = ['name', 'ona_pk']

    def __str__(self):
        return self.name
