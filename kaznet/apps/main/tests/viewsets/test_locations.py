"""
Tests Main Location viewsets.
"""
import os

import pytz
from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework_gis.fields import GeoJsonDict
from tasking.common_tags import (GEODETAILS_ONLY, GEOPOINT_MISSING,
                                 RADIUS_MISSING)

from kaznet.apps.main.models import Location
from kaznet.apps.main.tests.base import MainTestBase
from kaznet.apps.main.viewsets import KaznetLocationViewSet
from kaznet.apps.users.tests.base import create_admin_user

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class TestKaznetLocationViewSet(MainTestBase):
    """
    Test LocationViewSet class.
    """

    def setUp(self):
        super(TestKaznetLocationViewSet, self).setUp()
        self.factory = APIRequestFactory()

    def _create_location(self):
        """
        Helper to create a single location
        """
        user = create_admin_user()

        data = {
            'name': 'Nairobi',
            'country': 'KE',
        }
        view = KaznetLocationViewSet.as_view({'post': 'create'})
        request = self.factory.post('/locations', data)
        # Need authenticated user
        force_authenticate(request, user=user)
        response = view(request=request)

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual('Nairobi', response.data['name'])
        self.assertDictContainsSubset(data, response.data)
        return response.data

    def test_create_location(self):
        """
        Test POST /locations adding a new location.
        """
        self._create_location()

    def test_create_location_with_shapefile(self):
        """
        Test that we can create a Location Object with a shapefile
        """
        user = create_admin_user()
        path = os.path.join(
            BASE_DIR, 'fixtures', 'test_shapefile.zip')

        with open(path, 'r+b') as shapefile:
            data = {
                'name': 'Nairobi',
                'country': 'KE',
                'shapefile': shapefile
            }
            view = KaznetLocationViewSet.as_view({'post': 'create'})
            request = self.factory.post('/locations', data)
            # Need authenticated user
            force_authenticate(request, user=user)
            response = view(request=request)

            self.assertEqual(response.status_code, 201, response.data)
            self.assertEqual('Nairobi', response.data['name'])
            self.assertEqual(type(response.data['shapefile']), GeoJsonDict)

    def test_create_with_bad_data(self):
        """
        Test that we get appropriate errors when trying to create an object
        with bad data
        """
        bob_user = create_admin_user()

        data_missing_radius = {
            'name': 'Nairobi',
            'geopoint': '30,10',
            }
        view = KaznetLocationViewSet.as_view({'post': 'create'})
        request = self.factory.post('/locations', data_missing_radius)
        # Need authenticated user
        force_authenticate(request, user=bob_user)
        response = view(request=request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(RADIUS_MISSING,
                         str(response.data[0]['detail']))

        data_missing_geopoint = {
            'name': 'Montreal',
            'radius': 45.678
            }

        view1 = KaznetLocationViewSet.as_view({'post': 'create'})
        request1 = self.factory.post('/locations', data_missing_geopoint)
        # Need authenticated user
        force_authenticate(request1, user=bob_user)
        response1 = view1(request=request1)

        self.assertEqual(response1.status_code, 400)
        self.assertEqual(GEOPOINT_MISSING,
                         str(response1.data[0]['detail']))

        path = os.path.join(
            BASE_DIR, 'fixtures', 'test_shapefile.zip')

        with open(path, 'r+b') as shapefile:
            data_shapefile = dict(
                name='Arusha',
                radius=56.6789,
                geopoint='30,10',
                shapefile=shapefile
                )

            view2 = KaznetLocationViewSet.as_view({'post': 'create'})
            request2 = self.factory.post('/locations', data_shapefile)
            # Need authenticated user
            force_authenticate(request2, user=bob_user)
            response2 = view2(request=request2)

            self.assertEqual(response2.status_code, 400)
            self.assertEqual(GEODETAILS_ONLY,
                             str(response2.data[0]['detail']))

    def test_delete_location(self):
        """
        Test DELETE location.
        """
        user = create_admin_user()
        location = mommy.make('main.Location')

        # assert that location exists
        self.assertTrue(Location.objects.filter(pk=location.id).exists())
        # delete location
        view = KaznetLocationViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('/locations/{id}'.format(id=location.id))
        force_authenticate(request, user=user)
        response = view(request=request, pk=location.id)
        # assert that location was deleted
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Location.objects.filter(pk=location.id).exists())

    def test_retrieve_location(self):
        """
        Test GET /locations/[pk] return a location matching pk.
        """
        user = create_admin_user()
        location_data = self._create_location()

        view = KaznetLocationViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(
            '/locations/{id}'.format(id=location_data['id']))
        force_authenticate(request, user=user)
        response = view(request=request, pk=location_data['id'])

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, location_data)

    def test_list_locations(self):
        """
        Test GET /locations listing of locations for specific forms.
        """
        user = create_admin_user()
        location_data = self._create_location()

        view = KaznetLocationViewSet.as_view({'get': 'list'})

        request = self.factory.get('/locations')
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        resp = response.data['results'].pop()
        self.assertDictEqual(resp, location_data)

    def test_update_location(self):
        """
        Test UPDATE location
        """
        user = create_admin_user()
        location_data = self._create_location()

        data = {
            'name': 'Arusha',
            'country': 'TZ',
        }

        view = KaznetLocationViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(
            '/locations/{id}'.format(id=location_data['id']), data=data)
        force_authenticate(request, user=user)
        response = view(request=request, pk=location_data['id'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual('Arusha', response.data['name'])
        self.assertEqual('TZ', response.data['country'])

    def test_parent_filter(self):
        """
        Test that you can filter by parent
        """
        user = create_admin_user()
        location1 = mommy.make('main.Location', name='Eldorado')
        location2 = mommy.make('main.Location', name='Africa')

        mommy.make(
            'main.Location',
            name='Market Town', parent=location2, _quantity=7)

        view = KaznetLocationViewSet.as_view({'get': 'list'})

        # assert that there are no locations with location1 as a parent
        request = self.factory.get('/locations?', {'parent': location1.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)
        self.assertEqual(
            Location.objects.filter(parent=location1).count(), 0)

        # assert that there are 7 locations with location2 as parent
        request = self.factory.get('/locations?', {'parent': location2.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 7)
        self.assertEqual(
            Location.objects.filter(parent=location2).count(), 7)

        # create a new location and make its parent location1 and assert that
        # it's there
        mommy.make('main.Location', name='Africa', parent=location1)

        request = self.factory.get('/locations?', {'parent': location1.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            Location.objects.filter(parent=location1).count(), 1)

    def test_country_filter(self):
        """
        Test that you can filter by country
        """
        user = create_admin_user()

        mommy.make(
            'main.Location',
            name='Market Town', country='US', _quantity=7)

        view = KaznetLocationViewSet.as_view({'get': 'list'})

        # assert that there are no locations in Kenya(KE)
        request = self.factory.get('/locations?', {'country': 'KE'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)
        self.assertEqual(
            Location.objects.filter(country='KE').count(), 0)

        # assert that there are 7 locations in the United States(US)
        request = self.factory.get('/locations?', {'country': 'US'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 7)
        self.assertEqual(
            Location.objects.filter(country='US').count(), 7)

        # create a new location with country Kenya(KE) and assert its there
        mommy.make('main.Location', name='Nairobi', country='KE')

        request = self.factory.get('/locations?', {'country': 'KE'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            Location.objects.filter(country='KE').count(), 1)

    def test_name_search(self):
        """
        Test that you can search by Name
        """
        user = create_admin_user()
        mommy.make('main.Location', name='Eldorado')
        mommy.make('main.Location', name='Market', _quantity=7)

        view = KaznetLocationViewSet.as_view({'get': 'list'})
        request = self.factory.get('/locations', {'search': 'Eldorado'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            Location.objects.filter(name='Eldorado').count(), 1)

    def test_location_sorting(self):
        """
        Test that sorting works
        """
        user = create_admin_user()
        project1 = mommy.make('main.Location', name='Nairobi')
        project2 = mommy.make('main.Location', name='Arusha')

        view = KaznetLocationViewSet.as_view({'get': 'list'})

        # order by name descending
        request = self.factory.get('/locations', {'ordering': '-name'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(
            response.data['results'][0]['name'], project1.name)
        self.assertEqual(response.data['results'][0]['id'], project1.id)
        self.assertEqual(
            response.data['results'][-1]['name'], project2.name)
        self.assertEqual(response.data['results'][-1]['id'], project2.id)

        # order by created ascending
        request = self.factory.get('/locations', {'ordering': 'created'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(
            response.data['results'][0]['created'],
            project1.created.astimezone(
                pytz.timezone('Africa/Nairobi')).isoformat())
        self.assertEqual(response.data['results'][0]['id'], project1.id)
        self.assertEqual(
            response.data['results'][-1]['created'],
            project2.created.astimezone(
                pytz.timezone('Africa/Nairobi')).isoformat())
        self.assertEqual(response.data['results'][-1]['id'], project2.id)

    # pylint: disable=too-many-locals
    def test_authentication_required(self):
        """
        Test that authentication is required for all viewset actions
        """
        location_data = self._create_location()
        location1_data = self._create_location()
        location = mommy.make('main.Location')

        # test that you need authentication for creating a location
        data = {
            'name': 'Nairobi',
            'country': 'KE',
            }

        view = KaznetLocationViewSet.as_view({'post': 'create'})
        request = self.factory.post('/locations', data)

        response = view(request=request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            str(response.data[0]['detail']))

        # test that you need authentication for retrieving a location
        view1 = KaznetLocationViewSet.as_view({'get': 'retrieve'})
        request1 = self.factory.get(
            '/locations/{id}'.format(id=location_data['id']))
        response1 = view1(request=request1, pk=location_data['id'])

        self.assertEqual(response1.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            str(response1.data[0]['detail']))

        # test that you need authentication for listing a task
        view2 = KaznetLocationViewSet.as_view({'get': 'list'})
        request2 = self.factory.get('/locations')
        response2 = view2(request=request2)

        self.assertEqual(response2.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            str(response2.data[0]['detail']))

        # test that you need authentication for deleting a task
        # assert that location exists
        self.assertTrue(Location.objects.filter(pk=location.id).exists())

        view3 = KaznetLocationViewSet.as_view({'delete': 'destroy'})
        request3 = self.factory.delete(
            '/locations/{id}'.format(id=location.id))
        response3 = view3(request=request3, pk=location.id)

        self.assertEqual(response3.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            str(response3.data[0]['detail']))

        # test that you need authentication for updating a task
        data2 = {
            'name': 'Arusha',
            'country': 'TZ',
        }

        view4 = KaznetLocationViewSet.as_view({'patch': 'partial_update'})
        request4 = self.factory.patch(
            '/locations/{id}'.format(id=location1_data['id']), data=data2)
        response4 = view4(request=request4, pk=location1_data['id'])

        self.assertEqual(response4.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            str(response4.data[0]['detail']))

    def test_permission_required(self):
        """
        Test permissions required to access API Endpoints
        """
        user = mommy.make('auth.User')
        # Cant Delete

        location = mommy.make('main.Location')

        # pylint: disable=no-member
        self.assertTrue(Location.objects.filter(pk=location.id).exists())
        view = KaznetLocationViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('/locations/{id}'.format(id=location.id))
        force_authenticate(request, user)
        response = view(request=request, pk=location.id)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'You shall not pass.',
            str(response.data[0]['detail']))

        # Cant Update

        data = {
            'name': "Solair",
            }

        view = KaznetLocationViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(
            '/locations/{id}'.format(id=location.id), data=data)
        force_authenticate(request, user)
        response = view(request=request, pk=location.id)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'You shall not pass.',
            str(response.data[0]['detail']))

        # Cant Create

        data = {
            'name': 'Flux Company'
        }

        view = KaznetLocationViewSet.as_view({'post': 'create'})
        request = self.factory.post('/locations', data)
        force_authenticate(request, user)
        response = view(request=request)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'You shall not pass.',
            str(response.data[0]['detail']))

        # Cant List

        mommy.make('main.Location', name='Solair')
        mommy.make('main.Location', name='Generic', _quantity=7)

        view = KaznetLocationViewSet.as_view({'get': 'list'})
        request = self.factory.get('/locations')
        force_authenticate(request, user)
        response = view(request=request)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'You shall not pass.',
            str(response.data[0]['detail']))

        # Cant Retrieve

        client = mommy.make('main.Location', name='Bob')

        view = KaznetLocationViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('/locations/{id}'.format(id=client.id))
        force_authenticate(request, user)
        response = view(request=request, pk=location.id)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'You shall not pass.',
            str(response.data[0]['detail']))
