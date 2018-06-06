"""
Tests module for ClientViewSet
"""

from django.test import TestCase

from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate

from kaznet.apps.main.models import Client
from kaznet.apps.main.viewsets import ClientViewSet
from kaznet.apps.users.tests.base import create_admin_user


class TestClientViewSet(TestCase):
    """
    Test for ClientViewSet
    """

    def setUp(self):
        super(TestClientViewSet, self).setUp()
        self.factory = APIRequestFactory()

    def test_create_client(self):
        """
        Test that a user with required permissions can create
        a client
        """
        user = create_admin_user()

        data = {
            'name': 'Flux Company'
        }

        view = ClientViewSet.as_view({'post': 'create'})
        request = self.factory.post('/tasks', data)
        # Need authenticated user
        force_authenticate(request, user=user)
        response = view(request=request)

        self.assertEqual(response.status_code, 201)
        self.assertDictContainsSubset(data, response.data)

        # pylint: disable=no-member
        client = Client.objects.get(pk=response.data['id'])

        self.assertEqual(client.name, data['name'])

    def test_list_clients(self):
        """
        Test GET /client returns all clients
        """
        user = create_admin_user()
        mommy.make('main.Client', name='Solair')
        mommy.make('main.CLient', name='Generic', _quantity=7)

        view = ClientViewSet.as_view({'get': 'list'})
        request = self.factory.get('/client')
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 8)

    def test_retrieve_client(self):
        """
        Test GET /client/[pk] return a client matching pk.
        """
        user = create_admin_user()
        client = mommy.make('main.Client', name='Bob')

        view = ClientViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('/client/{id}'.format(id=client.id))
        force_authenticate(request, user=user)
        response = view(request=request, pk=client.id)
        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.data['name'], client.name)

    def test_name_search(self):
        """
        Test that you can search by name
        """
        user = create_admin_user()
        mommy.make('main.Client', name='Solair')
        mommy.make('main.CLient', name='Generic', _quantity=7)

        view = ClientViewSet.as_view({'get': 'list'})
        request = self.factory.get('/client', {'search': 'Solair'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            # pylint: disable=no-member
            Client.objects.filter(name='Solair').count(), 1)

    def test_name_ordering(self):
        """
        Test that we can order list by name
        """
        user = create_admin_user()
        client1 = mommy.make('main.Client', name='Bee Happy')
        mommy.make('main.CLient', name='Generic', _quantity=7)
        client2 = mommy.make('main.Client', name='Zero Company')

        # Test we can sort by name in ascending order
        view = ClientViewSet.as_view({'get': 'list'})
        request = self.factory.get('/client', {'ordering': 'name'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 9)
        self.assertEqual(response.data[0]['name'], client1.name)
        self.assertEqual(response.data[0]['id'], client1.id)
        self.assertEqual(response.data[-1]['name'], client2.name)
        self.assertEqual(response.data[-1]['id'], client2.id)

    def test_update_client(self):
        """
        Test that we can update a client
        """
        user = create_admin_user()
        client = mommy.make('main.Client')

        data = {
            'name': "Solair",
            }

        view = ClientViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(
            '/client/{id}'.format(id=client.id), data=data)
        force_authenticate(request, user=user)
        response = view(request=request, pk=client.id)

        self.assertEqual(response.status_code, 200)
        # pylint: disable=no-member
        client = Client.objects.get(pk=client.id)
        self.assertEqual(client.name, 'Solair')

    def test_delete_client(self):
        """
        Test DELETE /client/[pk] deletes a client matching pk
        """
        user = create_admin_user()
        client = mommy.make('main.Client')

        # assert that task exists
        # pylint: disable=no-member
        self.assertTrue(Client.objects.filter(pk=client.id).exists())
        # delete task
        view = ClientViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('/client/{id}'.format(id=client.id))
        force_authenticate(request, user=user)
        response = view(request=request, pk=client.id)
        # assert that task was deleted
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Client.objects.filter(pk=client.id).exists())

    def test_authentication_required(self):
        """
        Test that user needs to be authenticated
        """
        # Cant Delete

        client = mommy.make('main.Client')

        # pylint: disable=no-member
        self.assertTrue(Client.objects.filter(pk=client.id).exists())
        view = ClientViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('/client/{id}'.format(id=client.id))
        response = view(request=request, pk=client.id)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            str(response.data['detail']))

        # Cant Update

        data = {
            'name': "Solair",
            }

        view = ClientViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(
            '/tasks/{id}'.format(id=client.id), data=data)
        response = view(request=request, pk=client.id)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            str(response.data['detail']))

        # Cant Create

        data = {
            'name': 'Flux Company'
        }

        view = ClientViewSet.as_view({'post': 'create'})
        request = self.factory.post('/tasks', data)
        response = view(request=request)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            str(response.data['detail']))

        # Cant List

        mommy.make('main.Client', name='Solair')
        mommy.make('main.CLient', name='Generic', _quantity=7)

        view = ClientViewSet.as_view({'get': 'list'})
        request = self.factory.get('/client')
        response = view(request=request)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            str(response.data['detail']))

        # Cant Retrieve

        client = mommy.make('main.Client', name='Bob')

        view = ClientViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('/client/{id}'.format(id=client.id))
        response = view(request=request, pk=client.id)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            str(response.data['detail']))

    def test_permission_required(self):
        """
        Test that user requires permission to access the API Endpoint
        """

        user = mommy.make('auth.User')
        # Cant Delete

        client = mommy.make('main.Client')

        # pylint: disable=no-member
        self.assertTrue(Client.objects.filter(pk=client.id).exists())
        view = ClientViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('/client/{id}'.format(id=client.id))
        force_authenticate(request, user)
        response = view(request=request, pk=client.id)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'You shall not pass.',
            str(response.data['detail']))

        # Cant Update

        data = {
            'name': "Solair",
            }

        view = ClientViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(
            '/tasks/{id}'.format(id=client.id), data=data)
        force_authenticate(request, user)
        response = view(request=request, pk=client.id)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'You shall not pass.',
            str(response.data['detail']))

        # Cant Create

        data = {
            'name': 'Flux Company'
        }

        view = ClientViewSet.as_view({'post': 'create'})
        request = self.factory.post('/tasks', data)
        force_authenticate(request, user)
        response = view(request=request)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'You shall not pass.',
            str(response.data['detail']))

        # Cant List

        mommy.make('main.Client', name='Solair')
        mommy.make('main.CLient', name='Generic', _quantity=7)

        view = ClientViewSet.as_view({'get': 'list'})
        request = self.factory.get('/client')
        force_authenticate(request, user)
        response = view(request=request)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'You shall not pass.',
            str(response.data['detail']))

        # Cant Retrieve

        client = mommy.make('main.Client', name='Bob')

        view = ClientViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('/client/{id}'.format(id=client.id))
        force_authenticate(request, user)
        response = view(request=request, pk=client.id)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'You shall not pass.',
            str(response.data['detail']))
