# -*- coding: utf-8 -*-
"""
URLs module for main Kaznet app
"""
from django.contrib import admin

from kaznet.apps.main.models import (Bounty, Client, Location, LocationType,
                                     Project, Submission, Task, TaskLocation,
                                     TaskOccurrence)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """
    Admin Definition for Location Model
    """
    list_display = (
        'name',
        'country',
    )
    list_filter = ('created', 'modified', 'parent')
    search_fields = ('name',)


@admin.register(TaskOccurrence)
class TaskOccurrenceAdmin(admin.ModelAdmin):
    """
    Admin Definition for TaskOccurrence Model
    """
    list_display = (
        'id',
        'task',
        'date',
        'start_time',
        'end_time',
    )
    list_filter = ('created', 'modified', 'date', 'task')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin Definition for Project Model
    """
    list_display = (
        'name',
    )
    list_filter = ('created', 'modified', 'target_content_type')
    raw_id_fields = ('tasks',)
    search_fields = ('name',)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    """
    Admin Definition for Submission Model
    """
    list_display = (
        'id',
        'user',
        'task',
        'bounty',
        'location',
        'submission_time',
        'valid',
        'status',
    )
    list_filter = (
        'created',
        'modified',
        'target_content_type',
        'user',
        'submission_time',
        'valid',
        'task',
        'bounty',
        'location',
    )
    date_hierarchy = 'submission_time'
    search_fields = ('task__name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin Definition for Task Model
    """
    list_display = (
        'name',
        'parent',
        'start',
        'end',
        'status',
        'client',
    )
    list_filter = (
        'created',
        'modified',
        'target_content_type',
        'parent',
        'start',
        'end',
        'client',
    )
    raw_id_fields = ('segment_rules', 'locations')
    search_fields = ('name',)
    date_hierarchy = 'start'


@admin.register(Bounty)
class BountyAdmin(admin.ModelAdmin):
    """
    Admin Definition for Bounty Model
    """
    list_display = ('id', 'task', 'amount')
    list_filter = ('created', 'task')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Admin Definition for Client Model
    """
    list_display = ('name',)
    list_filter = ('created', 'modified')
    search_fields = ('name',)


@admin.register(LocationType)
class LocationTypeAdmin(admin.ModelAdmin):
    """
    Admin definition for LocationType
    """
    list_display = ('name',)
    list_filter = ('created', 'modified')
    search_fields = ('name',)


@admin.register(TaskLocation)
class TaskLocationAdmin(admin.ModelAdmin):
    """
    Admin definition for TaskLocation
    """
    list_display = (
        'id',
        'task',
        'location',
        'timing_rule',
        'start',
        'end',
    )
    list_filter = ('created', 'modified', 'task', 'location')
    search_fields = ('task__name',)
