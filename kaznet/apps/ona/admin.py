# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import XForm, Instance, Project


@admin.register(XForm)
class XFormAdmin(admin.ModelAdmin):
    """
    Admin definition for XForm
    """
    list_display = (
        'id',
        'title',
        'id_string',
    )
    list_filter = ('created', 'modified', 'deleted_at', 'last_updated')


@admin.register(Instance)
class InstanceAdmin(admin.ModelAdmin):
    """
    Admin definition for Instance
    """
    list_display = (
        'id',
        'ona_pk',
        'xform',
        'user',
    )
    list_filter = (
        'created',
        'modified',
        'xform',
        'deleted_at',
        'user',
        'last_updated',
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin definition for Project
    """
    list_display = (
        'id',
        'ona_pk',
        'organization',
        'name',
    )
    list_filter = ('created', 'modified', 'deleted_at', 'last_updated')
    search_fields = ('name',)
