import unittest
from app import create_app

class FlaskAppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up a test instance of the Flask app."""
        cls.app = create_app('testing')
        cls.client = cls.app.test_client()

    def test_homepage(self):
        """Test if the homepage loads successfully."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome", response.data)

    def test_weather_endpoint(self):
        """Test the weather endpoint with a valid city."""
        response = self.client.get('/weather?city=London')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"temperature", response.data)

    def test_weather_endpoint_invalid_city(self):
        """Test the weather endpoint with an invalid city."""
        response = self.client.get('/weather?city=InvalidCity')
        self.assertEqual(response.status_code, 404)

    def test_form_submission(self):
        """Test form submission for valid data."""
        response = self.client.post('/submit', data={'field_name': 'value'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Form submitted successfully", response.data)

    def test_form_submission_invalid_data(self):
        """Test form submission with missing or invalid data."""
        response = self.client.post('/submit', data={}, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
