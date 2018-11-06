"""
Test for SegmentRule models
"""

from model_mommy import mommy

from kaznet.apps.main.tests.base import MainTestBase


class TestSegmentRule(MainTestBase):
    """
    Test class for SegmentRule models
    """

    def setUp(self):
        super().setUp()

    def test_segment_rule_model_str(self):
        """
        Test the str method on SegmentRule model
        """
        rule0 = mommy.make('main.SegmentRule', name='Rule Zero')
        self.assertEqual('Rule Zero', rule0.__str__())
