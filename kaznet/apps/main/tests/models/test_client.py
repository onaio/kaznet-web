"""
Test for Client model
"""
from model_mommy import mommy


class TestClient():
    """
    Test client model class
    """
    def test_client_str(self):

        client = mommy.make('main.Client', name="slug org")
        expected = "slug org"

        self.assertEqual(expected, client.__str__())
