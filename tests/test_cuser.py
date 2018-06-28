import unittest
import json
from app import create_app, db

class FlaskClientTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('Test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_login(self):
        response = self.client.post('http://localhost:5000/api/cusers/session', data=json.dumps({}))
        self.assertTrue('Username is required.' in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/cusers/session', data=json.dumps({
            "username": "dfd",
        }))
        self.assertTrue('Successfully login.' in response.get_data(as_text=True))

    def test_logout(self):
        response = self.client.put('http://localhost:5000/api/cusers/session')
        self.assertTrue('Login required.' in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/cusers/session', data=json.dumps({
            "username": "dfaad",
        }))
        self.assertTrue('Successfully login.' in response.get_data(as_text=True))

        response = self.client.put('http://localhost:5000/api/cusers/session')
        self.assertTrue('Successfully logout.' in response.get_data(as_text=True))

