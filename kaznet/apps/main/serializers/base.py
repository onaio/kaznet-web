"""
Kaznet Base Serializers
"""
from rest_framework_json_api import serializers
from tasking.common_tags import TARGET_DOES_NOT_EXIST
from tasking.utils import get_allowed_contenttypes


def validate_parent_field(instance, value):
    """
    Check if parent field is valid
    """
    return instance is not None and value == instance


# pylint: disable=too-many-ancestors
class ContentTypeFieldSerializer(serializers.ModelSerializer):
    """
    Serializer class that provides a contenty_type field
    """
    target_content_type = serializers.PrimaryKeyRelatedField(
        many=False, queryset=get_allowed_contenttypes())


# pylint: disable=too-many-ancestors
class GenericForeignKeySerializer(ContentTypeFieldSerializer):
    """
    Serializer class that provides fields and methods for dealing
    with generic foreign keys
    """

    target_id = serializers.IntegerField(
        source='target_object_id', required=False)

    def validate(self, attrs):
        """
        Validate target id
        """
        if self.instance is not None:
            # we are doing an update
            target_id = attrs.get(
                'target_object_id', self.instance.target_object_id)
            target_model_contenttype = attrs.get(
                'target_content_type', self.instance.target_content_type)
        else:
            # we are creating a new object
            target_id = attrs.get('target_object_id')
            target_model_contenttype = attrs.get('target_content_type')

        # Target_id is not required as such this may be none
        # If target_id is none there is no need to validate it
        if target_id is not None:
            target_model_class = target_model_contenttype.model_class()

            try:
                target_model_class.objects.get(pk=target_id)
            except target_model_class.DoesNotExist:
                raise serializers.ValidationError(
                    {'target_id': TARGET_DOES_NOT_EXIST}
                )

            return attrs
        return attrs
