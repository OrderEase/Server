import unittest
import json
from flask import current_app
from app import db
import app.gen_data as data_generator

class FlaskClientTest(unittest.TestCase):

    def setUp(self):

        self.client = current_app.test_client()
        response = self.client.post('http://localhost:5000/api/busers/session', data=json.dumps({
            "username": "manager",
            "password": "123"
        }))
        self.assertTrue("Successfully login." in response.get_data(as_text=True))


    def tearDown(self):
        response = self.client.put('http://localhost:5000/api/busers/session')
        self.assertTrue('Successfully logout.' in response.get_data(as_text=True))

    def test_turnover(self):
        response = self.client.get('http://localhost:5000/api/analytics/turnover?days=7')
        self.assertTrue(response.status_code == 200)
        # print(response.get_data(as_text=True))

        response = self.client.get('http://localhost:5000/api/analytics/turnover?days=30')
        self.assertTrue(response.status_code == 200)
        # print(response.get_data(as_text=True))

    def test_countCard(self):
        response = self.client.get('http://localhost:5000/api/analytics/count/card')
        self.assertTrue(response.status_code == 200)
        # print(response.get_data(as_text=True))

    def test_payway(self):
        response = self.client.get('http://localhost:5000/api/analytics/count/payway')
        # print(response.get_data(as_text=True))
        self.assertTrue(response.status_code == 200)

    def test_countOrders(self):
        response = self.client.get('http://localhost:5000/api/analytics/count/orders')
        # print(response.get_data(as_text=True))
        self.assertTrue(response.status_code == 200)

    def test_countFinishTime(self):
        response = self.client.get('http://localhost:5000/api/analytics/count/finishtime')
        # print(response.get_data(as_text=True))
        self.assertTrue(response.status_code == 200)

    def test_rankLikes(self):
        response = self.client.get('http://localhost:5000/api/analytics/rank/likes')
        # print(response.get_data(as_text=True))
        self.assertTrue(response.status_code == 200)

    def test_rankSale(self):
        response = self.client.get('http://localhost:5000/api/analytics/rank/sales')
        # print(response.get_data(as_text=True))
        self.assertTrue(response.status_code == 200)

    def test_summary(self):
        response = self.client.get('http://localhost:5000/api/analytics/summary?start=2018-06-10&end=2018-06-16')
        # print(response.get_data(as_text=True))
        self.assertTrue(response.status_code == 200)

        response = self.client.get('http://localhost:5000/api/analytics/summary')
        # print(response.get_data(as_text=True))
        self.assertTrue(response.status_code == 200)

