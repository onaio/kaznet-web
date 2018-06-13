"""
Tests module for main Task viewsets.
"""

from datetime import timedelta

from django.utils import six, timezone

import pytz
from dateutil.parser import parse
from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate
from tasking.common_tags import TARGET_DOES_NOT_EXIST

from kaznet.apps.main.models import Task
from kaznet.apps.main.tests.base import MainTestBase
from kaznet.apps.main.viewsets import KaznetTaskViewSet
from kaznet.apps.users.tests.base import create_admin_user


class TestKaznetTaskViewSet(MainTestBase):
    """
    Test KaznetTaskViewSet class.
    """

    def setUp(self):
        super(TestKaznetTaskViewSet, self).setUp()
        self.factory = APIRequestFactory()

    def _create_task(self):
        """
        Helper to create a single task
        """
        mocked_target_object = mommy.make('ona.XForm')

        user = create_admin_user()

        data = {
            'name': 'Cow price',
            'description': 'Some description',
            'total_submission_target': 10,
            'timing_rule': 'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            'target_content_type': self.xform_type.id,
            'target_id': mocked_target_object.id,
        }

        view = KaznetTaskViewSet.as_view({'post': 'create'})
        request = self.factory.post('/tasks', data)
        # Need authenticated user
        force_authenticate(request, user=user)
        response = view(request=request)

        self.assertEqual(response.status_code, 201, response.data)
        self.assertDictContainsSubset(data, response.data)

        # start and end were gotten from timing_rule
        # lets check that they are correct by compating it to the start and
        # end values of the Task object that was created
        the_task = Task.objects.get(pk=response.data['id'])

        # the start and end in the_task are UTC, we convert response.data to
        # UTC so that we can compare
        utc_start = parse(response.data['start']).astimezone(pytz.utc)
        utc_end = parse(response.data['end']).astimezone(pytz.utc)

        self.assertEqual(utc_start, the_task.start)
        self.assertEqual(utc_end, the_task.end)

        return response.data

    def test_create_task(self):
        """
        Test POST /tasks adding a new task.
        """
        self._create_task()

    def test_create_with_bad_data(self):
        """
        Test that we get appropriate errors when trying to create an object
        with bad data
        """
        bob_user = create_admin_user()
        mocked_target_object = mommy.make('ona.XForm')

        # test bad target_id validation
        bad_target_id = dict(
            name='Cow price',
            description='Some description',
            start=timezone.now(),
            total_submission_target=10,
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            target_content_type=self.xform_type.id,
            target_id=1337,
        )

        view1 = KaznetTaskViewSet.as_view({'post': 'create'})
        request1 = self.factory.post('/tasks', bad_target_id)
        # Need admin user
        force_authenticate(request1, user=bob_user)
        response1 = view1(request=request1)

        self.assertEqual(response1.status_code, 400)
        self.assertEqual(TARGET_DOES_NOT_EXIST,
                         six.text_type(response1.data[0]['detail']))

        # test bad content type validation
        bad_content_type = dict(
            name='Cow price',
            description='Some description',
            start=timezone.now(),
            total_submission_target=10,
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            target_content_type=999,
            target_object_id=mocked_target_object.id,
        )

        view2 = KaznetTaskViewSet.as_view({'post': 'create'})
        request2 = self.factory.post('/tasks', bad_content_type)
        # Need admin user
        force_authenticate(request2, user=bob_user)
        response2 = view2(request=request2)

        self.assertEqual(response2.status_code, 400)
        self.assertEqual(
            'Invalid pk "999" - object does not exist.',
            six.text_type(response2.data[0]['detail']))

    def test_delete_task(self):
        """
        Test DELETE tasks.
        """
        user = create_admin_user()
        task = mommy.make('main.Task')

        # assert that task exists
        self.assertTrue(Task.objects.filter(pk=task.id).exists())
        # delete task
        view = KaznetTaskViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('/tasks/{id}'.format(id=task.id))
        force_authenticate(request, user=user)
        response = view(request=request, pk=task.id)
        # assert that task was deleted
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Task.objects.filter(pk=task.id).exists())

    def test_retrieve_task(self):
        """
        Test GET /tasks/[pk] return a task matching pk.
        """
        user = mommy.make('auth.User')
        task = mommy.make('main.Task')
        view = KaznetTaskViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('/tasks/{id}'.format(id=task.id))
        force_authenticate(request, user=user)
        response = view(request=request, pk=task.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], task.id)

    def test_list_tasks(self):
        """
        Test GET /tasks listing of tasks for specific forms.
        """
        user = mommy.make('auth.User')
        task = mommy.make('main.Task')
        view = KaznetTaskViewSet.as_view({'get': 'list'})

        request = self.factory.get('/tasks')
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['id'], task.id)

    def test_update_task(self):
        """
        Test UPDATE task
        """
        user = create_admin_user()
        xform = mommy.make('ona.XForm')
        task_data = self._create_task()
        task_data2 = self._create_task()

        data = {
            'name': "Milk Price",
            'target_content_type': self.xform_type.id,
            'target_id': xform.id,
            }

        view = KaznetTaskViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(
            '/tasks/{id}'.format(id=task_data['id']), data=data)
        force_authenticate(request, user=user)
        response = view(request=request, pk=task_data['id'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual('Milk Price', response.data['name'])
        self.assertEqual(
            self.xform_type.id,
            response.data['target_content_type'])
        self.assertEqual(xform.id, response.data['target_id'])

        data2 = {
            'name': "Cattle Price",
            'description': 'Hello there!',
            }

        view2 = KaznetTaskViewSet.as_view({'patch': 'partial_update'})
        request2 = self.factory.patch(
            '/tasks/{id}'.format(id=task_data2['id']), data=data2)
        force_authenticate(request2, user=user)
        response2 = view2(request=request2, pk=task_data2['id'])

        self.assertEqual(response2.status_code, 200)
        self.assertEqual('Cattle Price', response2.data['name'])
        self.assertEqual(
            'Hello there!',
            response2.data['description'])

    def test_clone_task(self):
        """
        Test Clone task
        """
        user = create_admin_user()
        task_data = self._create_task()

        data = {
            'id': task_data['id']
        }

        view = KaznetTaskViewSet.as_view({'post': 'clone_task'})
        request = self.factory.post(
            '/tasks/{id}/clone_task'.format(id=task_data['id']), data=data)
        force_authenticate(request, user=user)
        response = view(request=request, pk=task_data['id'])

        old_name = task_data['name']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            f'{old_name} - Copy', response.data['name'])
        self.assertEqual(None, response.data['target_content_type'])
        self.assertEqual(
            task_data['timing_rule'], response.data['timing_rule'])
        self.assertEqual(
            task_data['locations'], response.data['locations'])
        self.assertEqual(
            task_data['segment_rules'], response.data['segment_rules'])
        self.assertEqual(
            task_data['bounty'], response.data['bounty'])
        self.assertEqual(
            'd', response.data['status']
        )

    # pylint: disable=too-many-locals
    def test_authentication_required(self):
        """
        Test that authentication is required for all viewset actions
        """
        mocked_target_object = mommy.make('ona.XForm')
        task_data = self._create_task()
        task = mommy.make('main.Task')
        xform = mommy.make('ona.XForm')

        # test that you need authentication for creating a task
        good_data = {
            'name': 'Cow price',
            'description': 'Some description',
            'start': timezone.now(),
            'total_submission_target': 10,
            'timing_rule': 'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            'target_content_type': self.xform_type.id,
            'target_id': mocked_target_object.id,
        }
        view = KaznetTaskViewSet.as_view({'post': 'create'})
        request = self.factory.post('/tasks', good_data)
        response = view(request=request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response.data[0]['detail']))

        # test that you need authentication for retrieving a task
        view2 = KaznetTaskViewSet.as_view({'get': 'retrieve'})
        request2 = self.factory.get('/tasks/{id}'.format(id=task_data['id']))
        response2 = view2(request=request2, pk=task_data['id'])
        self.assertEqual(response2.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response2.data[0]['detail']))

        # test that you need authentication for listing a task
        view3 = KaznetTaskViewSet.as_view({'get': 'list'})
        request3 = self.factory.get('/tasks')
        response3 = view3(request=request3)
        self.assertEqual(response3.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response3.data[0]['detail']))

        # test that you need authentication for deleting a task
        self.assertTrue(Task.objects.filter(pk=task.id).exists())

        view4 = KaznetTaskViewSet.as_view({'delete': 'destroy'})
        request4 = self.factory.delete('/tasks/{id}'.format(id=task.id))
        response4 = view4(request=request4, pk=task.id)

        self.assertEqual(response4.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response4.data[0]['detail']))

        # test that you need authentication for updating a task
        data = {
            'name': "Milk Price",
            'target_content_type': self.xform_type.id,
            'target_id': xform.id,
            }

        view5 = KaznetTaskViewSet.as_view({'patch': 'partial_update'})
        request5 = self.factory.patch(
            '/tasks/{id}'.format(id=task_data['id']), data=data)
        response5 = view5(request=request5, pk=task_data['id'])

        self.assertEqual(response5.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response5.data[0]['detail']))

    def test_location_filter(self):
        """
        Test that you can filter by location
        """
        user = mommy.make('auth.User')
        nairobi = mommy.make('main.Location', name='Nairobi')
        arusha = mommy.make('main.Location', name='Arusha')
        for _ in range(0, 7):
            task = mommy.make('main.Task')
            task.locations.add(nairobi)

        view = KaznetTaskViewSet.as_view({'get': 'list'})

        # assert that there are no tasks for Arusha
        request = self.factory.get('/tasks', {'locations': arusha.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)
        self.assertEqual(Task.objects.filter(locations=arusha).count(), 0)

        # assert that there are 7 tasks for Nairobi
        request = self.factory.get('/tasks', {'locations': nairobi.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 7)
        self.assertEqual(Task.objects.filter(locations=nairobi).count(), 7)

        # add one Arusha task and assert that we get it back
        task2 = mommy.make('main.Task')
        task2.locations.add(arusha)
        request = self.factory.get('/tasks', {'locations': arusha.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(Task.objects.filter(locations=arusha).count(), 1)

    def test_parent_filter(self):
        """
        Test that you can filter by parent
        """
        user = mommy.make('auth.User')
        parent1 = mommy.make('main.Task')
        parent2 = mommy.make('main.Task')

        mommy.make('main.Task', parent=parent1, _quantity=7)

        view = KaznetTaskViewSet.as_view({'get': 'list'})

        # assert that there are no tasks whose parent is parent2
        request = self.factory.get('/tasks', {'parent': parent2.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)
        self.assertEqual(Task.objects.filter(parent=parent2.id).count(), 0)

        # assert that there are 7 tasks whose parent is parent1
        request = self.factory.get('/tasks', {'parent': parent1.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 7)
        self.assertEqual(Task.objects.filter(parent=parent1.id).count(), 7)

        # create a task whose parent is parent2 and assert its there
        mommy.make('main.Task', parent=parent2)

        request = self.factory.get('/tasks', {'parent': parent2.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(Task.objects.filter(parent=parent2.id).count(), 1)

    def test_status_filter(self):
        """
        Test that you can filter by status
        """
        user = mommy.make('auth.User')
        mommy.make('main.Task', status=Task.DEACTIVATED, _quantity=7)

        view = KaznetTaskViewSet.as_view({'get': 'list'})

        # assert that there are no tasks with an Active Status
        request = self.factory.get('/tasks', {'status': Task.ACTIVE})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)
        self.assertEqual(Task.objects.filter(status=Task.ACTIVE).count(), 0)

        # assert that there are 7 tasks with an Deactivated Status
        request = self.factory.get('/tasks', {'status': Task.DEACTIVATED})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 7)
        self.assertEqual(
            Task.objects.filter(status=Task.DEACTIVATED).count(), 7)

        # add a task with with an Active Status and assert that we get it back
        mommy.make('main.Task', status=Task.ACTIVE)
        request = self.factory.get('/tasks', {'status': Task.ACTIVE})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(Task.objects.filter(status=Task.ACTIVE).count(), 1)

    def test_project_filter(self):
        """
        Test that you can filter by Project
        """
        user = mommy.make('auth.User')
        project1 = mommy.make('main.Project', name='Test Case Scenario')
        project2 = mommy.make('main.Project', name='Reality Check')
        for _ in range(0, 7):
            task = mommy.make('main.Task')
            project1.tasks.add(task)

        view = KaznetTaskViewSet.as_view({'get': 'list'})
        # assert that there are no tasks in project Reality Check
        request = self.factory.get('/tasks', {'project': project2.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)
        self.assertEqual(
            Task.objects.filter(project=project2.id).count(), 0)

        # assert that there are 7 tasks in project Test Case Scenario
        request = self.factory.get('/tasks', {'project': project1.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 7)
        self.assertEqual(
            Task.objects.filter(project=project1.id).count(), 7)

        # add a task to project Reality Check and assert its there
        task2 = mommy.make('main.Task')
        project2.tasks.add(task2)

        request = self.factory.get('/tasks', {'project': project2.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            Task.objects.filter(project=project2.id).count(), 1)

    def test_name_search(self):
        """
        Test that you can search by Name
        """
        user = mommy.make('auth.User')
        mommy.make('main.Task', name='Cattle Price')
        mommy.make('main.Task', name='Chicken Price', _quantity=7)

        view = KaznetTaskViewSet.as_view({'get': 'list'})
        request = self.factory.get('/tasks', {'search': 'Cattle Price'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            Task.objects.filter(name='Cattle Price').count(), 1)

    def test_task_sorting(self):
        """
        Test that sorting works
        """
        user = mommy.make('auth.User')
        project1 = mommy.make('main.Project')
        project3 = mommy.make('main.Project')
        project2 = mommy.make('main.Project')
        task1 = mommy.make(
            'main.Task',
            name='Milk Production Size',
            status=Task.DRAFT,
            estimated_time=timedelta(4, 4520))
        project1.tasks.add(task1)

        for _ in range(0, 7):
            # create other tasks
            task = mommy.make(
                'main.Task',
                name='Cow Price',
                status=Task.DEACTIVATED,
                estimated_time=timedelta(3, 3250)
                )
            mommy.make('main.Submission', task=task, _quantity=3)
            project3.tasks.add(task)
        task2 = mommy.make(
            'main.Task',
            name='Allocated land for farming',
            status=Task.ACTIVE,
            estimated_time=timedelta(2, 4520))
        project2.tasks.add(task2)

        # Create and add Submissions to Task1 and Task2
        mommy.make('main.Submission', task=task1, _quantity=4)
        mommy.make('main.Submission', task=task2, _quantity=1)

        view = KaznetTaskViewSet.as_view({'get': 'list'})

        # order by status descending
        request = self.factory.get('/tasks', {'ordering': '-status'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.data['results'][0]['id'], task1.id)
        self.assertEqual(response.data['results'][0]['status'], task1.status)
        self.assertEqual(response.data['results'][-1]['id'], task2.id)
        self.assertEqual(response.data['results'][-1]['status'], task2.status)

        # order by created ascending
        request = self.factory.get('/tasks', {'ordering': 'created'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(
            parse(response.data['results'][0]['created']).astimezone(pytz.utc),
            task1.created)
        self.assertEqual(response.data['results'][0]['id'], task1.id)
        self.assertEqual(
            parse(
                response.data['results'][-1]['created']).astimezone(
                    pytz.utc),
            task2.created)
        self.assertEqual(response.data['results'][-1]['id'], task2.id)

        # order by name ascending
        request = self.factory.get('/tasks', {'ordering': 'name'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(
            response.data['results'][-1]['name'], task1.name)
        self.assertEqual(response.data['results'][-1]['id'], task1.id)
        self.assertEqual(
            response.data['results'][0]['name'], task2.name)
        self.assertEqual(response.data['results'][0]['id'], task2.id)

        # order by project ascending
        request = self.factory.get('/tasks', {'ordering': 'project__id'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(
            response.data['results'][0]['name'], task1.name)
        self.assertEqual(response.data['results'][0]['id'], task1.id)
        self.assertEqual(
            response.data['results'][-1]['name'], task2.name)
        self.assertEqual(response.data['results'][-1]['id'], task2.id)

        # order by submissions descending
        request = self.factory.get('/tasks', {'ordering': '-submission_count'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(
            response.data['results'][0]['name'], task1.name)
        self.assertEqual(response.data['results'][0]['id'], task1.id)
        self.assertEqual(
            response.data['results'][-1]['name'], task2.name)
        self.assertEqual(response.data['results'][-1]['id'], task2.id)
        self.assertTrue(task1.submissions > task2.submissions)

        # order by Estimated Time descending
        request = self.factory.get('/tasks', {'ordering': '-estimated_time'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(
            response.data['results'][0]['name'], task1.name)
        self.assertEqual(response.data['results'][0]['id'], task1.id)
        self.assertEqual(
            response.data['results'][-1]['name'], task2.name)
        self.assertEqual(response.data['results'][-1]['id'], task2.id)
        self.assertTrue(task1.estimated_time > task2.estimated_time)

    def test_search_filter_order(self):
        """
        Test that you can search filter and order at the same time
        """
        user = mommy.make('auth.User')

        task = mommy.make(
            'main.Task', name='Cattle Price', status=Task.ACTIVE)
        task2 = mommy.make(
            'main.Task', name='Cattle Price', status=Task.ACTIVE)

        mommy.make('main.Task', name='Cattle Price', status=Task.DRAFT)

        for _ in range(0, 4):
            mommy.make(
                'main.Task', name='Cattle Price', status=Task.DEACTIVATED)

        view = KaznetTaskViewSet.as_view({'get': 'list'})

        request = self.factory.get(
            '/tasks?search={name}&status={status}&ordering={order}'.format(
                name='Cattle Price', status=Task.ACTIVE, order='created'))
        force_authenticate(request, user=user)

        response = view(request=request)

        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['status'], task.status)
        self.assertEqual(response.data['results'][0]['id'], task.id)
        self.assertEqual(response.data['results'][1]['status'], task2.status)
        self.assertEqual(response.data['results'][1]['id'], task2.id)

    def test_latest_bounty_ordering(self):
        """
        Test that we can sort Tasks by latest_bounty amount
        """
        user = mommy.make('auth.User')

        task1 = mommy.make('main.Task', name='Cattle Price')
        task2 = mommy.make('main.Task', name='SpaceShip Price')
        task3 = mommy.make('main.Task', name='Earth Price')

        mommy.make('main.Bounty', amount=5000, task=task1)
        mommy.make('main.Bounty', amount=10000000, task=task2)
        mommy.make('main.Bounty', amount=10000, task=task3)

        view = KaznetTaskViewSet.as_view({'get': 'list'})

        # Test ordering ascending
        request = self.factory.get('/tasks', {'ordering': 'bounty__amount'})
        force_authenticate(request, user=user)
        response = view(request=request)

        self.assertEqual(
            response.data['results'][0]['bounty']['id'],
            task1.bounty.id)
        self.assertEqual(response.data['results'][0]['id'], task1.id)
        self.assertEqual(
            response.data['results'][1]['bounty']['id'],
            task3.bounty.id)
        self.assertEqual(response.data['results'][1]['id'], task3.id)
        self.assertEqual(
            response.data['results'][-1]['bounty']['id'],
            task2.bounty.id)
        self.assertEqual(response.data['results'][-1]['id'], task2.id)

        # Test ordering descending
        request = self.factory.get('/tasks', {'ordering': '-bounty__amount'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(
            response.data['results'][0]['bounty']['id'],
            task2.bounty.id)
        self.assertEqual(response.data['results'][0]['id'], task2.id)
        self.assertEqual(
            response.data['results'][1]['bounty']['id'],
            task3.bounty.id)
        self.assertEqual(response.data['results'][1]['id'], task3.id)
        self.assertEqual(
            response.data['results'][-1]['bounty']['id'],
            task1.bounty.id)
        self.assertEqual(response.data['results'][-1]['id'], task1.id)

    def test_date_filter(self):
        """
        Test that you can filter by date
        """
        user = mommy.make('auth.User')
        task = mommy.make('main.Task')
        task2 = mommy.make('main.Task')

        # remove any autocreated task occurrences
        # pylint: disable=no-member
        task.taskoccurrence_set.all().delete()
        task2.taskoccurrence_set.all().delete()

        # make a bunch of occurrences
        mommy.make(
            'main.TaskOccurrence',
            _quantity=7,
            task=task,
            date='2018-07-12')

        # make one occurrence using a unique date
        mommy.make('main.TaskOccurrence', task=task2, date='2017-09-09')

        view = KaznetTaskViewSet.as_view({'get': 'list'})

        # test that we get the task with our unique date
        request = self.factory.get('/tasks',
                                   {'date': '2017-09-09'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], task2.id)

        # make some tasks that happen after 2018-07-12
        mommy.make(
            'main.TaskOccurrence',
            _quantity=5,
            task=task,
            date='2018-11-11')

        # test that we can get tasks before or after a certain date
        request2 = self.factory.get('/tasks',
                                    {'date__gt': '2018-07-13', 'xxx': 23})
        force_authenticate(request2, user=user)
        response2 = view(request=request2)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(len(response2.data['results']), 1)
        self.assertEqual(response2.data['results'][0]['id'], task.id)

    def test_start_time_filter(self):
        """
        Test that you can filter by start_time
        """
        user = mommy.make('auth.User')
        view = KaznetTaskViewSet.as_view({'get': 'list'})
        task = mommy.make('main.Task')
        task2 = mommy.make('main.Task')

        # remove any autocreated tasks
        # pylint: disable=no-member
        task.taskoccurrence_set.all().delete()
        task2.taskoccurrence_set.all().delete()

        # make some occurrences that start at 7
        mommy.make(
            'main.TaskOccurrence', _quantity=5, task=task,
            start_time='07:00')

        # make some occurrences that happen after 9:00
        mommy.make(
            'main.TaskOccurrence', _quantity=6, task=task2,
            start_time='09:15')

        # test that we can get tasks before or after a certain time
        request2 = self.factory.get(
            '/tasks', {'start_time__gte': '09:15'})
        force_authenticate(request2, user=user)
        response2 = view(request=request2)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(len(response2.data['results']), 1)
        self.assertEqual(response2.data['results'][0]['id'], task2.id)

        # check that we can get tasks before a certain time
        request3 = self.factory.get(
            '/tasks', {'start_time__lt': '09:15'})
        force_authenticate(request3, user=user)
        response3 = view(request=request3)
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(len(response3.data['results']), 1)
        self.assertEqual(response3.data['results'][0]['id'], task.id)

    def test_end_time_filter(self):
        """
        Test that you can filter by end_time
        """
        user = mommy.make('auth.User')
        view = KaznetTaskViewSet.as_view({'get': 'list'})
        task = mommy.make('main.Task')
        task2 = mommy.make('main.Task')

        # make some occurrences that end at 5pm
        mommy.make(
            'main.TaskOccurrence', _quantity=5, task=task, end_time='17:00')

        # make some tasks that end after 9pm
        mommy.make(
            'main.TaskOccurrence', _quantity=6, task=task2,
            end_time='21:15')

        # test that we can get tasks before or after a certain time
        request2 = self.factory.get(
            '/tasks', {'end_time__gte': '21:15'})
        force_authenticate(request2, user=user)
        response2 = view(request=request2)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(len(response2.data['results']), 1)
        self.assertEqual(response2.data['results'][0]['id'], task2.id)

        # check that we can get tasks before a certain time
        request3 = self.factory.get(
            '/tasks', {'end_time__lt': '21:15'})
        force_authenticate(request3, user=user)
        response3 = view(request=request3)
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(len(response3.data['results']), 1)
        self.assertEqual(response3.data['results'][0]['id'], task.id)

    def test_client_filter(self):
        """
        Test that you can filter by client
        """
        user = mommy.make('auth.User')

        client1 = mommy.make('main.Client', name='Knight Order')
        client2 = mommy.make('main.Client', name='Sun Order')

        mommy.make('main.Task', client=client2, _quantity=7)

        # Test there is no Task under Client1
        view = KaznetTaskViewSet.as_view({'get': 'list'})
        request = self.factory.get(
            '/tasks?', {'client': client1.id})
        force_authenticate(request, user=user)
        response = view(request=request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)

        # Test there is 1 Task under Client1

        task = mommy.make('main.Task', client=client1)

        view = KaznetTaskViewSet.as_view({'get': 'list'})
        request = self.factory.get(
            '/tasks?', {'client': client1.id})
        force_authenticate(request, user=user)
        response = view(request=request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], task.id)

    def test_permission_required(self):
        """
        Test that Admin permission is required for POST, PATCH and
        DELETE API Requests
        """

        # Can't Create Task

        mocked_target_object = mommy.make('ona.XForm')

        rule1 = mommy.make('main.SegmentRule')
        rule2 = mommy.make('main.SegmentRule')

        user = mommy.make('auth.User')

        data = {
            'name': 'Cow price',
            'description': 'Some description',
            'total_submission_target': 10,
            'timing_rule': 'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            'target_content_type': self.xform_type.id,
            'target_id': mocked_target_object.id,
        }

        data_with_segment_rules = data.copy()
        data_with_segment_rules['segment_rules'] = [rule1.id, rule2.id]

        view = KaznetTaskViewSet.as_view({'post': 'create'})
        request = self.factory.post('/tasks', data_with_segment_rules)
        # Need authenticated user
        force_authenticate(request, user=user)
        response = view(request=request)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'You shall not pass.',
            response.data[0]['detail']
        )

        # Can't Update Task
        xform = mommy.make('ona.XForm')
        task_data = self._create_task()
        data = {
            'name': "Milk Price",
            'target_content_type': self.xform_type.id,
            'target_id': xform.id,
            }

        view = KaznetTaskViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(
            '/tasks/{id}'.format(id=task_data['id']), data=data)
        force_authenticate(request, user=user)
        response = view(request=request, pk=task_data['id'])

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'You shall not pass.',
            response.data[0]['detail']
        )

        # Can't Delete Task
        task = mommy.make('main.Task')

        # assert that task exists
        self.assertTrue(Task.objects.filter(pk=task.id).exists())
        # delete task
        view = KaznetTaskViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('/tasks/{id}'.format(id=task.id))
        force_authenticate(request, user=user)
        response = view(request=request, pk=task.id)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'You shall not pass.',
            response.data[0]['detail']
        )
