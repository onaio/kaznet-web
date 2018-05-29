"""
Serializers for users app
"""
from django.contrib.auth.models import User

from rest_framework import serializers

from kaznet.apps.users.adapter import AccountAdapter
from kaznet.apps.users.models import UserProfile


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

    class Meta(object):  # pylint:  disable=too-few-public-methods
        """
        class meta options
        """
        model = UserProfile
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'ona_pk',
            'ona_username',
            'mpesa_number',
            'phone_number',
            'role',
            'expertise',
            'gender',
            'national_id'
        ]
        # read_only_fields = ('ona_pk', 'id', 'ona_username')

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
        userprofile.mpesa_number = validated_data.get('mpesa_number')
        userprofile.phone_number = validated_data.get('phone_number')
        userprofile.role = validated_data.get('role')
        userprofile.gender = validated_data.get('gender')
        userprofile.national_id = validated_data.get('national_id')
        userprofile.expertise = validated_data.get('expertise')

        return userprofile

