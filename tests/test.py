import unittest
from app import create_app  # Assuming your Flask app is created using a factory pattern

class FlaskAppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up a test instance of the Flask app."""
        cls.app = create_app('testing')  # Pass the configuration for testing
        cls.client = cls.app.test_client()

    def test_homepage(self):
        """Test if the homepage loads successfully."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome", response.data)  # Update to match your homepage content

    def test_weather_endpoint(self):
        """Test the weather endpoint with a valid city."""
        response = self.client.get('/weather?city=London')  # Adjust endpoint name and params
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"temperature", response.data)  # Assuming "temperature" is in the response

    def test_weather_endpoint_invalid_city(self):
        """Test the weather endpoint with an invalid city."""
        response = self.client.get('/weather?city=InvalidCity')
        self.assertEqual(response.status_code, 404)  # Or other appropriate status code

    def test_form_submission(self):
        """Test form submission for valid data."""
        response = self.client.post('/submit', data={'field_name': 'value'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Form submitted successfully", response.data)  # Adjust message as needed

    def test_form_submission_invalid_data(self):
        """Test form submission with missing or invalid data."""
        response = self.client.post('/submit', data={}, follow_redirects=True)
        self.assertEqual(response.status_code, 400)  # Adjust status code as per validation logic

if __name__ == '__main__':
    unittest.main()
