"""
Tests Location Type viewsets.
"""
from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate

from kaznet.apps.main.models import LocationType
from kaznet.apps.main.tests.base import MainTestBase
from kaznet.apps.main.viewsets import KaznetLocationTypeViewSet
from kaznet.apps.users.tests.base import create_admin_user


class TestKaznetLocationTypeViewSet(MainTestBase):
    """
    Test KaznetLocationTypeViewSet class.
    """

    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()

    def _create_location_type(self):
        """
        Helper to create a single location type
        """

        user = create_admin_user()

        data = {
            'name': "Market",
        }

        view = KaznetLocationTypeViewSet.as_view({'post': 'create'})
        request = self.factory.post('/locationtypes', data)
        # Need authenticated user
        force_authenticate(request, user=user)
        response = view(request=request)

        self.assertEqual(response.status_code, 201, response.data)
        self.assertDictContainsSubset(data, response.data)
        return response.data

    def test_create_location_type(self):
        """
        Test POST /locationtypes adding a new project.
        """
        self._create_location_type()

    def test_delete_location_type(self):
        """
        Test DELETE locationtype.
        """
        user = create_admin_user()
        locationtype = mommy.make('main.LocationType')

        # pylint: disable=no-member
        self.assertTrue(
            LocationType.objects.filter(pk=locationtype.id).exists())

        view = KaznetLocationTypeViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(
            '/locationtypes/{id}'.format(id=locationtype.id))
        force_authenticate(request, user=user)
        response = view(request=request, pk=locationtype.id)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            LocationType.objects.filter(pk=locationtype.id).exists())

    def test_retrieve_location_type(self):
        """
        Test GET /locationtypes/[pk] return a project matching pk.
        """
        user = create_admin_user()
        locationtype_data = self._create_location_type()
        view = KaznetLocationTypeViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(
            '/locationtypes/{id}'.format(id=locationtype_data['id']))
        force_authenticate(request, user=user)
        response = view(request=request, pk=locationtype_data['id'])
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, locationtype_data)

    def test_list_location_type(self):
        """
        Test GET /locationtypes listing of locationtypes
        """
        user = create_admin_user()
        locationtype_data = self._create_location_type()
        view = KaznetLocationTypeViewSet.as_view({'get': 'list'})

        request = self.factory.get('/locationtypes')
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data['results'].pop(), locationtype_data)

    def test_update_location_type(self):
        """
        Test UPDATE locationtype
        """
        user = create_admin_user()
        locationtype_data = self._create_location_type()

        data = {
            'name': "Hospital",
            }

        view = KaznetLocationTypeViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(
            '/locationtypes/{id}'.format(
                id=locationtype_data['id']), data=data)
        force_authenticate(request, user=user)
        response = view(request=request, pk=locationtype_data['id'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual('Hospital', response.data['name'])

    def test_name_search(self):
        """
        Test that you can search by name
        """
        user = create_admin_user()
        mommy.make('main.LocationType', name='Market')
        mommy.make('main.LocationType', name='Generic', _quantity=7)

        view = KaznetLocationTypeViewSet.as_view({'get': 'list'})
        request = self.factory.get('/locationtype', {'search': 'Market'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            # pylint: disable=no-member
            LocationType.objects.filter(name='Market').count(), 1)

    def test_name_ordering(self):
        """
        Test that we can order list by name
        """
        user = create_admin_user()
        locationtype1 = mommy.make('main.LocationType', name='Actuary')
        mommy.make('main.LocationType', name='Clinic', _quantity=7)
        locationtype2 = mommy.make('main.LocationType', name='Hospital')

        # Test we can sort by name in ascending order
        view = KaznetLocationTypeViewSet.as_view({'get': 'list'})
        request = self.factory.get('/locationtype', {'ordering': 'name'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 9)
        self.assertEqual(
            response.data['results'][0]['name'], locationtype1.name)
        self.assertEqual(response.data['results'][0]['id'], locationtype1.id)
        self.assertEqual(
            response.data['results'][-1]['name'], locationtype2.name)
        self.assertEqual(response.data['results'][-1]['id'], locationtype2.id)
