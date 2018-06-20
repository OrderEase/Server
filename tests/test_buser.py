import unittest
from app import create_app, db

class FlaskClientTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # 注册测试用 buser
        response = self.client.post('http://localhost:5000/api/busers/', data={
            "username": "aaa",
            "password": "123",
            "authority": "manager"})

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register(self):
        response = self.client.post('http://localhost:5000/api/busers/', data={
            "username": "aaabbb",
            "password": "1232",
            "authority": "manager"})
        self.assertTrue(response.status_code == 200)

    def test_login(self):
        response = self.client.post('http://localhost:5000/api/busers/session', data={
            "username": "aaa",
            "password": "123"
        })
        # print(response.json)
        self.assertTrue("Successfully login." in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/busers/session', data={
            "username": "aada",
            "password": "123"
        })
        # print(response.json)
        self.assertTrue("Invalid username or password." in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/busers/session', data={
            "username": "aaa",
            "password": "1dd23"
        })
        # print(response.json)
        self.assertTrue("Invalid username or password." in response.get_data(as_text=True))

    def test_logout(self):
        response = self.client.put('http://localhost:5000/api/busers/session')
        self.assertTrue('Login required.' in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/busers/session', data={
            "username": "aaa",
            "password": "123",
        })

        response = self.client.put('http://localhost:5000/api/busers/session')
        self.assertTrue('Successfully logout.' in response.get_data(as_text=True))

