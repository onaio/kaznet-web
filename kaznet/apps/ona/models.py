"""
Models from Onadata

See: https://github.com/onaio/onadata
"""

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from tasking.models.base import TimeStampedModel

from kaznet.apps.main.models import Task
from kaznet.apps.ona.constants import MAX_ID_LENGTH, XFORM_TITLE_LENGTH
from kaznet.apps.ona.managers import GenericSoftDeleteManager


class Project(TimeStampedModel, models.Model):
    """
    Project model from onadata
    """
    ona_pk = models.PositiveIntegerField(
        _("Onadata Primary Key"),
        db_index=True,
        unique=True,
        blank=False)
    organization = models.PositiveIntegerField(
        _("Organization ID"),
        blank=True,
        null=True,
        default=None
        )
    name = models.CharField(max_length=255)
    deleted_at = models.DateTimeField(
        _('Deleted at'),
        null=True,
        blank=True,
        default=None)
    last_updated = models.DateTimeField(
        _('Last Updated'),
        null=True,
        blank=True,
        default=None)

    objects = GenericSoftDeleteManager()

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta Options for Project
        """
        ordering = ['name', 'ona_pk']

    def __str__(self):
        return self.name


class XForm(TimeStampedModel, models.Model):
    """
    XForm model from onadata
    """
    ona_pk = models.PositiveIntegerField(
        _("Onadata Primary Key"),
        db_index=True,
        unique=True,
        blank=False)
    ona_project_id = models.PositiveIntegerField(
        _("Project ID"),
        db_index=True,
        unique=False,
        blank=False)
    title = models.CharField(
        _('Title'),
        editable=False,
        max_length=XFORM_TITLE_LENGTH)
    id_string = models.SlugField(
        _('ID String'),
        editable=False,
        max_length=MAX_ID_LENGTH)
    deleted_at = models.DateTimeField(
        _('Deleted at'),
        blank=True,
        null=True,
        default=None)
    last_updated = models.DateTimeField(
        _('Last Updated'),
        null=True,
        blank=True,
        default=None)
    # db_column='project_custom' is provided to handle problems associated with project
    # field and the move from project_id to ona_project_id
    project = models.ForeignKey(
        Project,
        db_column='project_custom',
        verbose_name=_('Kaznet Project'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_('This references the Kaznet Project.')
    )

    objects = GenericSoftDeleteManager()

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta Options for XForm
        """
        ordering = ['title', 'id_string']
        unique_together = ('ona_project_id', 'id_string')

    def __str__(self):
        return self.title

    def get_task_queryset(self):
        """
        Returns the attached task object
        """
        # pylint: disable=no-member
        return Task.objects.filter(
            target_content_type__model='xform', target_object_id=self.id)

    def get_has_task(self):
        """
        Custom method that returns whether task has_task or not
        """
        return self.task.exists()  # pylint: disable=no-member

    @property
    def task(self):
        """
        Property to get the task
        """
        return self.get_task_queryset()

    @property
    def has_task(self):
        """
        Returns the has_task property for XForm
        """
        return self.get_has_task()


class Instance(TimeStampedModel, models.Model):
    """
    Instance model from onadata
    """
    ona_pk = models.PositiveIntegerField(
        _("Onadata Primary Key"),
        db_index=True,
        unique=True,
        blank=False)
    xform = models.ForeignKey(
        'ona.XForm',
        null=False,
        on_delete=models.PROTECT)
    json = JSONField(
        default=dict,
        null=False)
    deleted_at = models.DateTimeField(
        _('Deleted at'),
        null=True,
        blank=True,
        default=None)
    user = models.ForeignKey(
        'auth.User',
        null=False,
        on_delete=models.PROTECT)
    last_updated = models.DateTimeField(
        _('Last Updated'),
        null=True,
        blank=True,
        default=None)
    objects = GenericSoftDeleteManager()

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta Options for Instance
        """
        ordering = ['ona_pk', 'deleted_at']

    def get_task(self):
        """
        Get the task for this submission
        This might return None or might return a task
        """
        return self.xform.task.first()  # pylint: disable=no-member
