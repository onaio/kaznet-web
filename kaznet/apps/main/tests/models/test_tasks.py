# -*- coding: utf-8 -*-
"""
Test for Task model
"""
from __future__ import unicode_literals

from model_mommy import mommy

from kaznet.apps.main.tests.base import MainTestBase


class TestTasks(MainTestBase):
    """
    Test class for task models
    """

    def setUp(self):
        super().setUp()

    def test_task_model_str(self):
        """
        Test the str method on Task model
        """
        cow_price = mommy.make('main.Task', name="Cow prices")
        expected = 'Cow prices - {}'.format(cow_price.pk)
        self.assertEqual(expected, str(cow_price))

    def test_create_task_from_xform(self):
        """
        For every ona xform a signal is triggered to create
        a corresponding kaznet task
        """
        xform = mommy.make('ona.XForm')
        cattle_task = mommy.make(
            'main.Task',
            name='Cattle Price',
            target_content_object=xform
        )

        self.assertEqual(cattle_task.target_object_id, xform.id)
        self.assertEqual(cattle_task.target_content_type, self.xform_type)

    def test_created_by_name(self):
        """
        Test the `created_by_name` property
        """
        cate_user = mommy.make(
            'auth.User', username='cate', first_name='Cate', last_name='Doe')
        self.assertEqual(
            'Cate Doe',
            mommy.make('main.Task', created_by=cate_user).created_by_name
        )

    def test_client_name(self):
        """
        Test client name
        """
        self.assertEqual(
            'Zerg',
            mommy.make(
                'main.Task', client=mommy.make('main.Client', name="Zerg")
            ).client_name
        )

    def test_task_xform(self):
        """
        Test:
            - get_xform method
            - get_xform_title method
            - get_xform_id_string method
            - get_xform_version method
            - get_xform_owner method
            - get_xform_owner_url method

            - xform_title property
            - xform_id_string property
            - xform_version property
            - xform_owner property
            - xform_owner_url property
        """
        xform = mommy.make(
            'ona.XForm',
            title='Coconut',
            id_string='coconut828',
            version='v828',
            json=dict(
                owner="mosh",
                owner_url="http://example.com/mosh"
            ),
            ona_pk=200,
            ona_project_id=12389)
        # test when no xform
        task_no_xform = mommy.make('main.Task')
        self.assertEqual(None, task_no_xform.get_xform())
        self.assertEqual(None, task_no_xform.get_xform_title())
        self.assertEqual(None, task_no_xform.get_xform_id_string())
        self.assertEqual(None, task_no_xform.xform_title)
        self.assertEqual(None, task_no_xform.xform_id_string)
        # test when XForm
        task = mommy.make('main.Task', target_content_object=xform)
        self.assertEqual(xform, task.get_xform())
        self.assertEqual('Coconut', task.get_xform_title())
        self.assertEqual('coconut828', task.get_xform_id_string())
        self.assertEqual('v828', task.get_xform_version())
        self.assertEqual('mosh', task.get_xform_owner())
        self.assertEqual('http://example.com/mosh', task.get_xform_owner_url())

        self.assertEqual('Coconut', task.xform_title)
        self.assertEqual(200, task.xform_ona_id)
        self.assertEqual('coconut828', task.xform_id_string)
        self.assertEqual('v828', task.xform_version)
        self.assertEqual('mosh', task.xform_owner)
        self.assertEqual('http://example.com/mosh', task.xform_owner_url)
        self.assertEqual(12389, task.xform_project_id)

    def test_xform_title(self):
        """
        Test xForm title property

        """
        xform = mommy.make('ona.XForm', title="test")
        cattle_task = mommy.make(
            'main.Task',
            name='Cattle Price',
            target_content_object=xform
        )

        self.assertEqual(xform.title, cattle_task.xform_title)
