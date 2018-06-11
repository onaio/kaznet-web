# -*- coding: utf-8 -*-
"""
URLs module for main Kaznet app
"""
from django.contrib import admin

from kaznet.apps.main.models import (Bounty, Client, Location, Project,
                                     Submission, Task,
                                     TaskOccurrence)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'parent',
        'name',
        'country',
    )
    list_filter = ('created', 'modified', 'parent')
    search_fields = ('name',)


@admin.register(TaskOccurrence)
class TaskOccurrenceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        'start_time',
        'end_time',
        'task',
    )
    list_filter = ('created', 'modified', 'date', 'task')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )
    list_filter = ('created', 'modified', 'target_content_type')
    raw_id_fields = ('tasks',)
    search_fields = ('name',)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'submission_time',
        'valid',
        'status',
        'task',
        'bounty',
        'location',
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


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'parent',
        'name',
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
    list_display = ('id', 'task', 'amount')
    list_filter = ('created', 'task')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('created', 'modified')
    search_fields = ('name',)
