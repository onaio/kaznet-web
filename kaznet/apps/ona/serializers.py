"""
Model Serializers for Ona app
"""

from rest_framework import serializers
from kaznet.apps.ona.models import XForm, OnaInstance, OnaProject


class XFormSerializer(serializers.ModelSerializer):
    """
    Serializer for XForm Model
    """

    class Meta(object):
        """
        Meta Options for XForm Serializer
        """
        model = XForm
        fields = [
            'id',
            'ona_pk',
            'ona_project_id',
            'title',
            'id_string',
            'created',
            'modified',
            'deleted_at'
        ]


class OnaInstanceSerializer(serializers.ModelSerializer):
    """
    Serializer for OnaInstance Model
    """

    class Meta(object):
        """
        Meta Options for OnaInstance Serializer
        """
        model = OnaInstance
        fields = [
            'id',
            'ona_pk',
            'xform',
            'created',
            'modified',
            'json',
            'deleted_at'
        ]


class OnaProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for OnaProject Model
    """

    class Meta(object):
        """
        Meta Options for OnaProject Serializer
        """
        model = OnaProject
        fields = [
            'id',
            'ona_pk',
            'ona_organization',
            'created',
            'modified',
            'name',
            'deleted_at'
        ]
