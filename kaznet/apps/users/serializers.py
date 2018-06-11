"""
Serializers for users app
"""
from django.contrib.auth.models import User

from rest_framework_json_api import serializers

from kaznet.apps.users.models import UserProfile


# pylint: disable=too-many-ancestors
class UserSerializer(serializers.ModelSerializer):
    """
    UserSerializer class
    """

    class Meta(object):  # pylint:  disable=too-few-public-methods
        """
        meta options
        """
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer class for UserProfile model
    """
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    submission_count = serializers.SerializerMethodField()

    class Meta(object):  # pylint:  disable=too-few-public-methods
        """
        class meta options
        """
        model = UserProfile
        fields = [
            'id',
            'created',
            'modified',
            'first_name',
            'last_name',
            'email',
            'ona_pk',
            'ona_username',
            'payment_number',
            'approved_submissions',
            'rejected_submissions',
            'approval_rate',
            'amount_earned',
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
            'submission_count'
        ]

    def get_submission_count(self, obj):  # pylint: disable=no-self-use
        """
        Get the submission count
        """
        return obj.user.submission_set.count()

    def create(self, validated_data):
        """
        Custom create method to create User object then UserProfile object
        """
        # create the User object
        user_data = validated_data.pop('user')
        user_data['username'] = validated_data.get('ona_username')
        user = UserSerializer.create(UserSerializer(),
                                     validated_data=user_data)
        # populate the UserProfile object
        userprofile = user.userprofile
        userprofile.ona_pk = validated_data.get('ona_pk')
        userprofile.ona_username = user.username
        userprofile.payment_number = validated_data.get('payment_number')
        userprofile.phone_number = validated_data.get('phone_number')
        userprofile.role = validated_data.get('role')
        userprofile.gender = validated_data.get('gender')
        userprofile.national_id = validated_data.get('national_id')
        userprofile.expertise = validated_data.get('expertise')
        userprofile.save()

        return userprofile

    def update(self, instance, validated_data):
        """
        Custom update method for UserProfiles
        """
        # deal with the user object

        user = instance.user
        user_data = validated_data.pop('user')

        # you can't change username
        try:
            del user_data['username']
        except KeyError:
            pass

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
        instance.save()

        return instance
