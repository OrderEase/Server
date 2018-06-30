import unittest
from app import create_app, db
import json
import app.gen_data as data_generator
from flask import current_app

class FlaskClientTest(unittest.TestCase):

    gen_data = False

    promotions = [
    {
        "theme": "qqq",
        "begin": "2017-11-23 16:10",
        "end": "2017-11-23 16:10",
        "isend": 1
    },
    {
        "theme": "eee",
        "begin": "2017-06-11 5:10",
        "end": "2017-07-01 12:10",
        "isend": 0
    }]

    def setUp(self):
        self.client = current_app.test_client()

        if not self.gen_data:
            response = self.client.post('http://localhost:5000/api/busers/session', data=json.dumps({
                "username": "manager",
                "password": "123",
            }))
            self.assertTrue("Successfully login." in response.get_data(as_text=True))

            for promotion in self.promotions:
                response = self.client.post('http://localhost:5000/api/promotions/', data=json.dumps(promotion))
                # print(response.get_data(as_text=True))
                self.assertTrue(response.status_code == 200)

            response = self.client.post('http://localhost:5000/api/promotions/1/rules', data=json.dumps({
                'mode': 1,
                'requirement': 100,
                'discount': 10
            }))
            self.assertTrue(response.status_code == 200)

            # 退出
            response = self.client.put('http://localhost:5000/api/busers/session')

            self.gen_data = True

    def tearDown(self):
        pass

    def test_getPromotions(self):
        response = self.client.get('http://localhost:5000/api/promotions/')
        self.assertTrue('Login required.' in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/busers/session', data=json.dumps({
            "username": "manager",
            "password": "123",
        }))
        self.assertTrue("Successfully login." in response.get_data(as_text=True))

        response = self.client.get('http://localhost:5000/api/promotions/')
        self.assertTrue(response.status_code == 200)

        response = self.client.put('http://localhost:5000/api/busers/session')
        self.assertTrue('Successfully logout.' in response.get_data(as_text=True))

    def test_getSinglePromotion(self):
        response = self.client.post('http://localhost:5000/api/busers/session', data=json.dumps({
            "username": "manager",
            "password": "123",
        }))
        self.assertTrue("Successfully login." in response.get_data(as_text=True))

        response = self.client.get('http://localhost:5000/api/promotions/1')
        # print(response.get_data(as_text=True))
        self.assertTrue(response.status_code == 200)

        response = self.client.put('http://localhost:5000/api/busers/session')
        self.assertTrue('Successfully logout.' in response.get_data(as_text=True))

    def test_add_delete_Promotion(self):
        pid = 0

        response = self.client.post('http://localhost:5000/api/promotions/', data=json.dumps({
            "theme": "端午节活动",
            "begin": "2017-11-23 16:10",
            "end": "2017-11-23 16:10",
            "isend": 1
        }))
        # print(response.get_data(as_text=True))
        self.assertTrue('Login required.' in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/busers/session', data=json.dumps({
            "username": "manager",
            "password": "123",
        }))
        # print(response.get_data(as_text=True))
        self.assertTrue("Successfully login." in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/promotions/', data=json.dumps({
            "theme": "端午节活动",
            "begin": "2017-11-23 16:10",
            "end": "2017-11-23 16:10",
            "isend": 1
        }))
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        pid = data.get('id')
        self.assertTrue(response.status_code == 200)

        response = self.client.delete('http://localhost:5000/api/promotions/%d' % pid)
        # print(response.get_data(as_text=True))
        self.assertTrue('delete promotion successfully.' in response.get_data(as_text=True))

        response = self.client.get('http://localhost:5000/api/promotions/%d' % pid)
        # print(response.get_data(as_text=True))
        self.assertTrue('promotion not found.' in response.get_data(as_text=True))

        response = self.client.put('http://localhost:5000/api/busers/session')
        self.assertTrue('Successfully logout.' in response.get_data(as_text=True))

    def test_modifyPromotions(self):
        pid = 0

        response = self.client.post('http://localhost:5000/api/busers/session', data=json.dumps({
            "username": "manager",
            "password": "123",
        }))
        self.assertTrue("Successfully login." in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/promotions/', data=json.dumps({
            "theme": "端午节活动",
            "begin": "2017-11-23 16:10",
            "end": "2017-11-23 16:10",
            "isend": 1
        }))
        self.assertTrue(response.status_code == 200)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        pid = data.get('id')

        response = self.client.put('http://localhost:5000/api/promotions/%d' % pid, data=json.dumps({
            "theme": "hhh",
            "begin": "2017-01-01 16:10",
            "end": "2017-01-02 16:10",
            "isend": 0
        }))
        # print(response.get_data(as_text=True))
        self.assertTrue('modify promotion successfully' in response.get_data(as_text=True))

        response = self.client.get('http://localhost:5000/api/promotions/%d' % pid)
        # print(response.get_data(as_text=True))
        self.assertTrue('hhh' in response.get_data(as_text=True))

        response = self.client.put('http://localhost:5000/api/busers/session')
        self.assertTrue('Successfully logout.' in response.get_data(as_text=True))
