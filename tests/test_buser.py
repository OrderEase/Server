import unittest
from app import create_app, db

class FlaskClientTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        response = self.client.post('http://localhost:5000/api/buser/', data={"restId": 1,
            "username": "aaa",
            "role": "BUSSINES",
            "password": "123",
            "authority": "MANAGER"})

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register(self):
        response = self.client.post('http://localhost:5000/api/buser/', data={"restId": 1,
            "username": "aaabbb",
            "role": "BUSSINES",
            "password": "123",
            "authority": "MANAGER"})
        self.assertTrue(response.status_code == 200)

    def test_login(self):
        response = self.client.post('http://localhost:5000/api/buser/session', data={
            "username": "aaa",
            "restId": 1,
            "password": "123",
            "role": "BUSSINES"
        })
        # print(response.json)
        self.assertTrue("Successfully login." in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/buser/session', data={
            "username": "aada",
            "restId": 1,
            "password": "123",
            "role": "BUSSINES"
        })
        # print(response.json)
        self.assertTrue("Username not exist." in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/buser/session', data={
            "username": "aaa",
            "restId": 1,
            "password": "1dd23",
            "role": "BUSSINES"
        })
        # print(response.json)
        self.assertTrue("Wrong password." in response.get_data(as_text=True))

    def test_logout(self):
        response = self.client.put('http://localhost:5000/api/buser/session')
        self.assertTrue('Login required.' in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/buser/session', data={
            "username": "aaa",
            "restId": 1,
            "password": "123",
            "role": "BUSSINES"
        })

        response = self.client.put('http://localhost:5000/api/buser/session')
        self.assertTrue('Successfully logout.' in response.get_data(as_text=True))

