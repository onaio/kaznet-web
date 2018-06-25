"""
Model Serializers for Ona app
"""

from rest_framework_json_api import serializers

from kaznet.apps.ona.models import Instance, Project, XForm


# pylint: disable=too-many-ancestors
class XFormSerializer(serializers.ModelSerializer):
    """
    Serializer for XForm Model
    """
    has_task = serializers.SerializerMethodField()

    class Meta(object):  # pylint: disable=too-few-public-methods
        """
        Meta Options for XForm Serializer
        """
        model = XForm
        fields = [
            'id',
            'ona_pk',
            'project_id',
            'last_updated',
            'title',
            'id_string',
            'created',
            'modified',
            'deleted_at',
            'has_task'
        ]

    def get_has_task(self, obj):  # pylint: disable=no-self-use
        """
        Get the form's task
        """
        return obj.task.exists()


class InstanceSerializer(serializers.ModelSerializer):
    """
    Serializer for OnaInstance Model
    """

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta Options for Instance Serializer
        """
        model = Instance
        fields = [
            'id',
            'ona_pk',
            'xform',
            'created',
            'modified',
            'last_updated',
            'json',
            'deleted_at'
        ]


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for OnaProject Model
    """

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta Options for Project Serializer
        """
        model = Project
        fields = [
            'id',
            'ona_pk',
            'organization',
            'last_updated',
            'created',
            'modified',
            'name',
            'deleted_at'
        ]
