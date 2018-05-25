import unittest
from app import create_app, db

class FlaskClientTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login(self):
        response = self.client.post('http://localhost:5000/api/cuser/session', data={
            "username": "dfd",
            "role": "CUSTOMER"
        })
        self.assertTrue('Successfully login.' in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/cuser/session', data={
            "username": "dddfd",
            "role": "OTHERS"
        })
        self.assertTrue('User role must be CUSTOMER.' in response.get_data(as_text=True))

    def test_logout(self):
        response = self.client.put('http://localhost:5000/api/cuser/session')
        # print(response.status_code)
        self.assertTrue('Login required.' in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/cuser/session', data={
            "username": "dfaad",
            "role": "CUSTOMER"
        })
        self.assertTrue('Successfully login.' in response.get_data(as_text=True))

        response = self.client.put('http://localhost:5000/api/cuser/session')
        # print(response.json)
        self.assertTrue('Successfully logout.' in response.get_data(as_text=True))

