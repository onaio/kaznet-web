"""
Serializers for users app
"""
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db.models.query import QuerySet

from rest_framework_json_api import serializers

from kaznet.apps.main.serializers.bounty import SerializableAmountField
from kaznet.apps.users.api import (add_team_member, create_ona_user,
                                   update_details)
from kaznet.apps.users.common_tags import (CANNOT_ACCESS_ONADATA,
                                           NEED_PASSWORD_ON_CREATE)
from kaznet.apps.users.models import UserProfile


class SerializableAvgAmountEarnedField(serializers.Field):
    """
    Custom Field for Avg Amount Earned
    """

    def to_representation(self, value):
        """
        Custom to representation for SerializableAvgAmountEarned Field
        """
        return f'{value} {settings.KAZNET_DEFAULT_CURRENCY}'

    def to_internal_value(self, data):
        """
        Custom to_internal_value for SerializableAvgAmountEarned Field
        """
        return data


# pylint: disable=too-many-ancestors
class UserSerializer(serializers.ModelSerializer):
    """
    UserSerializer class
    """

    class Meta:  # pylint:  disable=too-few-public-methods
        """
        meta options
        """
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'last_login',
            'password'
            )


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer class for UserProfile model
    """
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(
        source='user.password',
        allow_null=True,
        default=None,
        required=False,
        write_only=True)
    last_login = serializers.DateTimeField(
        source='user.last_login', read_only=True)
    submission_count = serializers.SerializerMethodField()
    amount_earned = SerializableAmountField(read_only=True)
    avg_amount_earned = SerializableAvgAmountEarnedField(read_only=True)
    metadata = serializers.JSONField(read_only=True)

    class Meta:  # pylint:  disable=too-few-public-methods
        """
        class meta options
        """
        model = UserProfile
        fields = [
            'id',
            'created',
            'modified',
            'role_display',
            'gender_display',
            'expertise_display',
            'first_name',
            'last_name',
            'password',
            'email',
            'ona_pk',
            'ona_username',
            'payment_number',
            'approved_submissions',
            'rejected_submissions',
            'approval_rate',
            'amount_earned',
            'last_login',
            'avg_submissions',
            'avg_approved_submissions',
            'avg_rejected_submissions',
            'avg_approval_rate',
            'avg_amount_earned',
            'phone_number',
            'role',
            'expertise',
            'gender',
            'national_id',
            'submission_count',
            'address',
            'metadata'
        ]

    owner_only_fields = ('metadata',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and hasattr(self.Meta, 'owner_only_fields'):
            request = self.context.get('request')
            is_permitted = (
                request and request.user and
                request.user == self.instance.user)
            if isinstance(self.instance, QuerySet) or not is_permitted or \
                    not request:
                for field in getattr(self.Meta, 'owner_only_fields'):
                    self.fields.pop(field)

    def get_submission_count(self, obj):  # pylint: disable=no-self-use
        """
        Get the submission count
        """
        return obj.user.submission_set.count()

    def validate_password(self, value):
        """
        Custom validation for Password Field
        """
        if not self.instance:
            # On create of a new user Password shouldn't be none
            if value is None:
                raise serializers.ValidationError(
                    NEED_PASSWORD_ON_CREATE
                )

        if value is not None:
            validate_password(value)

        return value

    def create(self, validated_data):
        """
        Custom create method to create User object then UserProfile object
        """
        user_data = validated_data.pop('user')
        user_data['username'] = validated_data.get('ona_username')
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')
        email = user_data.get('email')
        password = user_data.get('password')

        created, data = create_ona_user(
            settings.ONA_BASE_URL,
            user_data['username'],
            first_name,
            last_name,
            email,
            password
        )

        if not created:
            raise serializers.ValidationError(
                data
            )

        if not data:
            raise serializers.ValidationError(CANNOT_ACCESS_ONADATA)

        ona_pk = data.get('id')
        metadata = data.get('metadata')
        gravatar = data.get('gravatar')

        add_team_member(
            settings.ONA_BASE_URL,
            user_data['username'],
            settings.ONA_MEMBERS_TEAM_ID)

        # set an unusable password by not passing the password to the create
        # method.  Why, you ask?  Because we don't want to store passwords
        # on the Kaznet site.  Ona is the source of truth for this.
        try:
            del user_data['password']
        except KeyError:
            pass

        # create the User object
        user = UserSerializer.create(UserSerializer(),
                                     validated_data=user_data)
        # populate the UserProfile object
        userprofile = user.userprofile
        userprofile.ona_pk = ona_pk
        userprofile.ona_username = user.username
        userprofile.payment_number = validated_data.get('payment_number')
        userprofile.phone_number = validated_data.get('phone_number')
        if validated_data.get('role'):
            userprofile.role = validated_data.get('role')
        userprofile.gender = validated_data.get('gender')
        if validated_data.get('national_id'):
            userprofile.national_id = validated_data.get('national_id')
        userprofile.expertise = validated_data.get('expertise')

        if metadata:
            userprofile.metadata['last_password_edit'] = metadata.get(
                settings.ONA_LAST_PASSWORD_EDIT_FIELD)
        userprofile.metadata['gravatar'] = gravatar
        userprofile.save()

        return userprofile

    def update(self, instance, validated_data):
        """
        Custom update method for UserProfiles
        """
        # deal with the user object
        user = instance.user
        user_data = validated_data.pop('user')
        username = user.username
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')
        email = user_data.get('email')

        # you can't change username
        try:
            del user_data['username']
        except KeyError:
            pass

        # you can't change email
        # this is because Onadata requires your current password when changing
        # the email.  And we cannot get the user's current password
        try:
            del user_data['email']
        except KeyError:
            pass

        # you can't change password
        # this is because Onadata requires your current password when changing
        # the password.  And we cannot get the user's current password
        try:
            del user_data['password']
        except KeyError:
            pass

        updated, data = update_details(
            settings.ONA_BASE_URL,
            username,
            first_name,
            last_name,
            email)

        if not updated:
            raise serializers.ValidationError(
                data
            )

        if not data:
            raise serializers.ValidationError(CANNOT_ACCESS_ONADATA)

        metadata = data.get('metadata')
        gravatar = data.get('gravatar')

        UserSerializer().update(instance=user, validated_data=user_data)

        # deal with the userprofile object
        instance.payment_number = validated_data.get(
            'payment_number', instance.payment_number)
        instance.phone_number = validated_data.get('phone_number',
                                                   instance.phone_number)
        instance.role = validated_data.get('role', instance.role)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.national_id = validated_data.get('national_id',
                                                  instance.national_id)
        instance.expertise = validated_data.get('expertise',
                                                instance.expertise)

        if metadata:
            instance.metadata['last_password_edit'] = metadata.get(
                settings.ONA_LAST_PASSWORD_EDIT_FIELD)

        instance.metadata['gravatar'] = gravatar
        instance.save()

        return instance
