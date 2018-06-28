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

