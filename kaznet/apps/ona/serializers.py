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
    metadata = serializers.SerializerMethodField()

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta Options for XForm Serializer
        """
        model = XForm
        fields = [
            'id',
            'ona_pk',
            'ona_project_id',
            'last_updated',
            'title',
            'id_string',
            'version',
            'created',
            'modified',
            'deleted_at',
            'has_task',
            'project',
            'metadata'
        ]

    def get_metadata(self, obj):  # pylint: disable=no-self-use
        """
        Get metadata field
        """
        if obj:
            return obj.json
        return None


class InstanceSerializer(serializers.ModelSerializer):
    """
    Serializer for OnaInstance Model
    """

    # pylint: disable=too-few-public-methods
    class Meta:
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
    class Meta:
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
