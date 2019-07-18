"""
Tests for UserProfile serializers
"""
from urllib.parse import urljoin

from django.conf import settings
from django.contrib.auth.models import User
from django.test import override_settings

import requests_mock
from model_mommy import mommy

from kaznet.apps.main.tests.base import MainTestBase
from kaznet.apps.users.common_tags import NEED_PASSWORD_ON_CREATE
from kaznet.apps.users.models import UserProfile
from kaznet.apps.users.serializers import UserProfileSerializer
from kaznet.apps.main.models import Submission
from kaznet.apps.users.tests.base import generate_submissions


@override_settings(
    ONA_BASE_URL="https://kaznet.ona.io",
    ONA_ORG_NAME="kaznet",
    ONA_MEMBERS_TEAM_ID=1337,
    ONA_USERNAME="mosh"
)
class TestUserProfileSerializer(MainTestBase):
    """
    Test class for UserProfileSerializer
    """

    def setUp(self):
        super().setUp()

    def _create_user(self):
        """
        Utility to create users
        """
        with requests_mock.Mocker() as mocked:
            mocked.post(
                urljoin(settings.ONA_BASE_URL, 'api/v1/profiles'),
                status_code=201,
                json={'id': 1337})

            mocked.post(
                urljoin(
                    settings.ONA_BASE_URL,
                    f'api/v1/teams/{settings.ONA_MEMBERS_TEAM_ID}/members'),
                status_code=201)

            mocked.put(
                urljoin(
                    settings.ONA_BASE_URL,
                    f'api/v1/orgs/{settings.ONA_ORG_NAME}/members'),
                status_code=200)

            data = {
                'first_name': 'Bob',
                'last_name': 'Doe',
                'email': 'bobbie@example.com',
                'password': 'amalusceaNDb',
                'gender': UserProfile.MALE,
                'role': UserProfile.ADMIN,
                'expertise': UserProfile.EXPERT,
                'national_id': '123456789',
                'payment_number': '+254722222222',
                'phone_number': '+254722222222',
                'ona_pk': 1337,
                'ona_username': 'bobbie'
            }
            # pylint: disable=no-member
            self.assertFalse(
                UserProfile.objects.filter(user__username='bobbie').exists())
            serializer_instance = UserProfileSerializer(data=data)
            self.assertTrue(serializer_instance.is_valid())

            serializer_instance.save()
            self.assertTrue(
                UserProfile.objects.filter(user__username='bobbie').exists())

            # Uses Primary Key from Ona
            userprofile = UserProfile.objects.get(ona_username='bobbie')
            self.assertTrue(userprofile.ona_pk, 1337)

            # We remove password field Since password is write-only
            data.pop('password')

            self.assertDictContainsSubset(data, serializer_instance.data)

            # ensure that the User object has unusable password
            self.assertFalse(
                User.objects.get(username='bobbie').has_usable_password())

            return serializer_instance.data

    def test_create(self):
        """
        Test that you can create a user with the serializer
        """
        serializer_instance = self._create_user()

        fields = [
            'id', 'created', 'modified', 'first_name', 'last_name',
            'role_display', 'email', 'ona_pk', 'gender_display',
            'expertise_display', 'ona_username', 'payment_number',
            'phone_number', 'approval_rate', 'last_login', 'avg_submissions',
            'avg_rejected_submissions', 'avg_amount_earned',
            'avg_approval_rate', 'avg_approved_submissions',
            'rejected_submissions', 'amount_earned', 'approved_submissions',
            'role', 'expertise', 'gender', 'national_id', 'submission_count',
            'address', 'metadata'
        ]

        self.assertEqual(set(fields), set(serializer_instance.keys()))

    def test_update(self):
        """
        Test you can update a user with the serializer
        """
        initial_user_data = self._create_user()

        with requests_mock.Mocker() as mocked:
            data = {
                'first_name': 'Mosh',
                'last_name': 'Pitt',
                'email': 'mosh@example.com',  # cant edit this
                'role': UserProfile.CONTRIBUTOR,
                'expertise': UserProfile.INTERMEDIATE,
                'national_id': '1337',
                'payment_number': '+254722111111',
                'ona_pk': 9999,
            }

            # pylint: disable=no-member
            userprofile = UserProfile.objects.get(user__username='bobbie')
            mocked.patch(
                urljoin(settings.ONA_BASE_URL, f'api/v1/profiles/bobbie'),
                status_code=200,
                json={
                    'metadata': {
                        'last_password_edit': ''
                    },
                    'gravatar': ''
                })

            mocked.put(
                urljoin(
                    settings.ONA_BASE_URL,
                    f'api/v1/orgs/{settings.ONA_ORG_NAME}/members'),
                status_code=200)

            serializer_instance = UserProfileSerializer(
                instance=userprofile, data=data)
            self.assertTrue(serializer_instance.is_valid())
            serializer_instance.save()

            expected_data = dict(initial_user_data).copy()
            expected_data['first_name'] = 'Mosh'
            expected_data['last_name'] = 'Pitt'
            expected_data['email'] = 'bobbie@example.com'
            expected_data['role'] = UserProfile.CONTRIBUTOR
            expected_data['role_display'] = UserProfile.ROLE_CHOICES[1][1]
            expected_data['expertise_display'] = UserProfile.EXPERTISE_CHOICES[
                1][1]
            expected_data['expertise'] = UserProfile.INTERMEDIATE
            expected_data['national_id'] = '1337'
            expected_data['payment_number'] = '+254722111111'
            expected_data['metadata'] = {
                'gravatar': '',
                'last_password_edit': ''
            }

            # remove the modified field because it cannot be the same
            del expected_data['modified']

            self.assertDictContainsSubset(expected_data,
                                          serializer_instance.data)

            userprofile.refresh_from_db()

            self.assertEqual('Mosh', userprofile.user.first_name)
            self.assertEqual('Pitt', userprofile.user.last_name)
            self.assertEqual('bobbie@example.com', userprofile.user.email)
            self.assertEqual(UserProfile.ROLE_CHOICES[1][1],
                             userprofile.role_display)
            self.assertEqual(UserProfile.CONTRIBUTOR, userprofile.role)
            self.assertEqual(UserProfile.INTERMEDIATE, userprofile.expertise)
            self.assertEqual('1337', userprofile.national_id)
            self.assertEqual('+254722111111',
                             userprofile.payment_number.as_e164)

    def test_bad_data(self):
        """
        Test that the serializer will not accept bad data
        """

        # ensure that only valid phone numbers are accepted

        data = {
            'first_name': 'Bob',
            'last_name': 'Doe',
            'email': 'bobbie@example.com',
            'gender': UserProfile.MALE,
            'role': UserProfile.ADMIN,
            'expertise': UserProfile.EXPERT,
            'national_id': '123456789',
            'payment_number': '12345678',  # obviously bad
            'phone_number': '+254822222222',  # not valid for Kenya
            'ona_pk': 1337,
            'ona_username': 'bobbie'
        }
        serializer_instance = UserProfileSerializer(data=data)
        self.assertFalse(serializer_instance.is_valid())
        self.assertEqual(
            str(serializer_instance.errors['phone_number'][0]),
            'The phone number entered is not valid.')
        self.assertEqual(
            str(serializer_instance.errors['payment_number'][0]),
            'The phone number entered is not valid.')

        # test can't create userprofile without password
        data = {
            'first_name': 'Bob',
            'last_name': 'Doe',
            'email': 'bobbie@example.com',
            'gender': UserProfile.MALE,
            'role': UserProfile.ADMIN,
            'expertise': UserProfile.EXPERT,
            'national_id': '123456789',
            'payment_number': '+254722222222',
            'phone_number': '+254722222222',
            'ona_pk': 1337,
            'ona_username': 'bobbie'
        }

        serializer_instance = UserProfileSerializer(data=data)
        self.assertFalse(serializer_instance.is_valid())

        self.assertEqual(serializer_instance.errors['password'][0],
                         NEED_PASSWORD_ON_CREATE)

        # test that national_id, ona_pk, and ona_username are unique
        self._create_user()

        data = {
            'first_name': 'Bob',
            'last_name': 'Doe',
            'email': 'bobbie@example.com',
            'gender': UserProfile.MALE,
            'role': UserProfile.ADMIN,
            'expertise': UserProfile.EXPERT,
            'national_id': '123456789',
            'payment_number': '+254722222222',
            'phone_number': '+254722222222',
            'ona_pk': 1337,
            'ona_username': 'bobbie'
        }
        serializer_instance = UserProfileSerializer(data=data)
        self.assertFalse(serializer_instance.is_valid())
        self.assertEqual(
            str(serializer_instance.errors['national_id'][0]),
            'Profile with this National ID Number already exists.')
        self.assertEqual(
            str(serializer_instance.errors['ona_pk'][0]),
            'Profile with this Ona Primary key already exists.')
        self.assertEqual(
            str(serializer_instance.errors['ona_username'][0]),
            'Profile with this Ona Username already exists.')

    def test_password_validate(self):
        """
        Test Validates Password
        """

        data = {
            'first_name': 'Mosh',
            'last_name': 'Pitt',
            'password': 'ama',
            'email': 'mosh@example.com',
            'role': UserProfile.CONTRIBUTOR,
            'expertise': UserProfile.INTERMEDIATE,
            'national_id': '1337',
            'payment_number': '+254722111111',
            'ona_pk': 9999,
            'ona_username': 'mosh'
        }

        serializer_instance = UserProfileSerializer(data=data)
        self.assertFalse(serializer_instance.is_valid())
        self.assertEqual(
            str(serializer_instance.errors['password'][0]),
            'This password is too short. It must contain '
            'at least 8 characters.')

    def test_gender_and_gender_display(self):
        """
        Test gender field
        """
        userprofile = mommy.make("auth.User").userprofile
        serializer = UserProfileSerializer(userprofile)
        userprofile.gender = 1
        self.assertEqual(serializer.data["gender"], str(userprofile.gender))
        self.assertEqual(
            serializer.data["gender_display"], userprofile.gender_display)

        userprofile.gender = 2
        serializer = UserProfileSerializer(userprofile)
        self.assertEqual(serializer.data["gender"], str(userprofile.gender))
        self.assertEqual(
            serializer.data["gender_display"], userprofile.gender_display)

    def test_avg_approval_rate(self):
        """
        Test the avg_approval_property
        """
        userprofile = mommy.make("auth.User").userprofile
        generate_submissions(userprofile, Submission.APPROVED)

        serializer = UserProfileSerializer(userprofile)
        self.assertEqual(userprofile.avg_approval_rate,
                         serializer.data["avg_approval_rate"])

        generate_submissions(userprofile, Submission.APPROVED)

        serializer = UserProfileSerializer(userprofile)
        self.assertEqual(userprofile.avg_approval_rate,
                         serializer.data["avg_approval_rate"])

    def test_avg_amount_earned(self):
        """
        Test the avg_ammount_earned property
        """
        userprofile = mommy.make("auth.User").userprofile
        generate_submissions(userprofile, Submission.APPROVED)

        serializer = UserProfileSerializer(userprofile)
        self.assertEqual(str(userprofile.avg_amount_earned),
                         serializer.data["avg_amount_earned"][:-4])

        generate_submissions(userprofile, Submission.APPROVED)

        serializer = UserProfileSerializer(userprofile)
        self.assertEqual(str(userprofile.avg_amount_earned),
                         serializer.data["avg_amount_earned"][:-4])

    def test_avg_rejected_submissions(self):
        """
        Test avg_rejected_submission property
        """
        userprofile = mommy.make("auth.User").userprofile
        generate_submissions(userprofile, Submission.REJECTED)

        serializer = UserProfileSerializer(userprofile)
        self.assertEqual(userprofile.avg_rejected_submissions,
                         serializer.data["avg_rejected_submissions"])

        generate_submissions(userprofile, Submission.REJECTED)

        serializer = UserProfileSerializer(userprofile)
        self.assertEqual(userprofile.avg_rejected_submissions,
                         serializer.data["avg_rejected_submissions"])

    def test_avg_approved_submissions(self):
        """
        Test avg_approved_submissions property
        """
        userprofile = mommy.make("auth.User").userprofile
        generate_submissions(userprofile, Submission.APPROVED)

        serializer = UserProfileSerializer(userprofile)
        self.assertEqual(userprofile.avg_approved_submissions,
                         serializer.data["avg_approved_submissions"])

        generate_submissions(userprofile, Submission.APPROVED)

        serializer = UserProfileSerializer(userprofile)
        self.assertEqual(userprofile.avg_approved_submissions,
                         serializer.data["avg_approved_submissions"])

    def test_avg_submissions(self):
        """
        Test avg_approved_submissions property
        """
        userprofile = mommy.make("auth.User").userprofile
        generate_submissions(userprofile, Submission.APPROVED)

        serializer = UserProfileSerializer(userprofile)
        self.assertEqual(userprofile.avg_submissions,
                         serializer.data["avg_submissions"])

        generate_submissions(userprofile, Submission.APPROVED)

        serializer = UserProfileSerializer(userprofile)
        self.assertEqual(userprofile.avg_submissions,
                         serializer.data["avg_submissions"])

    def test_approval_rate(self):
        """
        Test approval_rate property
        """
        userprofile = mommy.make("auth.User").userprofile
        generate_submissions(userprofile, Submission.APPROVED)

        serializer = UserProfileSerializer(userprofile)
        self.assertEqual(userprofile.approval_rate,
                         serializer.data["approval_rate"])

        generate_submissions(userprofile, Submission.APPROVED)

        serializer = UserProfileSerializer(userprofile)
        self.assertEqual(userprofile.approval_rate,
                         serializer.data["approval_rate"])

    def test_approved_submissions(self):
        """
        Test approved_submissions property
        """
        userprofile = mommy.make("auth.User").userprofile
        generate_submissions(userprofile, Submission.APPROVED)

        serializer = UserProfileSerializer(userprofile)
        self.assertEqual(userprofile.approved_submissions,
                         serializer.data["approved_submissions"])

        generate_submissions(userprofile, Submission.APPROVED)

        serializer = UserProfileSerializer(userprofile)
        self.assertEqual(userprofile.approved_submissions,
                         serializer.data["approved_submissions"])

    def test_rejected_submissions(self):
        """
        Test rejected_submissions property
        """
        userprofile = mommy.make("auth.User").userprofile
        generate_submissions(userprofile, Submission.REJECTED)

        serializer = UserProfileSerializer(userprofile)
        self.assertEqual(userprofile.rejected_submissions,
                         serializer.data["rejected_submissions"])

        generate_submissions(userprofile, Submission.REJECTED)

        serializer = UserProfileSerializer(userprofile)
        self.assertEqual(userprofile.rejected_submissions,
                         serializer.data["rejected_submissions"])

    def test_payment_numer(self):
        """
        Test payment_number property
        """
        userprofile = mommy.make("auth.User").userprofile
        userprofile.payment_number = '+254722111111'
        serializer = UserProfileSerializer(userprofile)
        self.assertEqual(str(userprofile.payment_number.national_number),
                         serializer.data['payment_number'][-9:])
        userprofile.payment_number = '+254722222222'
        serializer = UserProfileSerializer(userprofile)
        self.assertEqual(str(userprofile.payment_number.national_number),
                         serializer.data['payment_number'][-9:])

    def test_national_id(self):
        """
        Test national_id field
        """
        userprofile = mommy.make("auth.User").userprofile
        userprofile.national_id = "33851788"
        serializer = UserProfileSerializer(userprofile)
        self.assertEqual(userprofile.national_id,
                         serializer.data["national_id"])

        userprofile.national_id = "89662488"
        serializer = UserProfileSerializer(userprofile)
        self.assertEqual(userprofile.national_id,
                         serializer.data["national_id"])

    def test_email(self):
        """
        Test email field
        """
        userprofile = mommy.make("auth.User").userprofile
        userprofile.user.email = "franklineapiyo@gmail.com"
        serializer = UserProfileSerializer(userprofile)
        self.assertEqual(userprofile.user.email, serializer.data["email"])

        userprofile.user.email = "apiyofrankline@gmail.com"
        serializer = UserProfileSerializer(userprofile)
        self.assertEqual(userprofile.user.email, serializer.data["email"])
