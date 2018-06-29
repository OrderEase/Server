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
            # print(response.get_data(as_text=True))
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
            self.assertTrue(200 == response.status_code)

            response = self.client.put('http://localhost:5000/api/busers/session')
            self.assertTrue('Successfully logout.' in response.get_data(as_text=True))

    def tearDown(self):
        pass

    def test_add_delete_Rule(self):
        rid = 0

        response = self.client.post('http://localhost:5000/api/promotions/1/rules', data=json.dumps({
            'mode': 1,
            'requirement': 100,
            'discount': 10
        }))
        self.assertTrue('Login required.' in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/busers/session', data=json.dumps({
            "username": "manager",
            "password": "123",
        }))
        self.assertTrue("Successfully login." in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/promotions/1/rules', data=json.dumps({
            'mode': 3,
            'requirement': 100,
            'discount': 10
        }))
        self.assertTrue('Mode is required to be 1 or 2.' in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/promotions/1/rules', data=json.dumps({
            'mode': 2,
            'requirement': -10,
            'discount': 10
        }))
        self.assertTrue('Requirement is required and not negative.' in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/promotions/1/rules', data=json.dumps({
            'mode': 1,
            'requirement': 100,
            'discount': 10
        }))
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        rid = data.get('id')
        self.assertTrue(200 == response.status_code)

        response = self.client.delete('http://localhost:5000/api/promotions/1/rules/%d' % rid)
        self.assertTrue(200 == response.status_code)

        response = self.client.delete('http://localhost:5000/api/promotions/1/rules/%d' % rid)
        self.assertTrue('rule not found' in response.get_data(as_text=True))

        response = self.client.put('http://localhost:5000/api/busers/session')
        self.assertTrue('Successfully logout.' in response.get_data(as_text=True))

    def test_getRule(self):
        rid = 0

        response = self.client.post('http://localhost:5000/api/promotions/1/rules', data=json.dumps({
            'mode': 1,
            'requirement': 100,
            'discount': 10
        }))
        self.assertTrue('Login required.' in response.get_data(as_text=True))

        # print(response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/busers/session', data=json.dumps({
            "username": "manager",
            "password": "123",
        }))
        self.assertTrue("Successfully login." in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/promotions/1/rules', data=json.dumps({
            'mode': 1,
            'requirement': 100,
            'discount': 10
        }))
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        rid = data.get('id')
        self.assertTrue(200 == response.status_code)

        response = self.client.get('http://localhost:5000/api/promotions/1/rules/%d' % rid)
        # print(response.get_data(as_text=True))
        self.assertTrue(200 == response.status_code)

        response = self.client.get('http://localhost:5000/api/promotions/1/rules/%d' % (rid + 1))
        # print(response.get_data(as_text=True))
        self.assertTrue('rule not found' in response.get_data(as_text=True))

        response = self.client.put('http://localhost:5000/api/busers/session')
        self.assertTrue('Successfully logout.' in response.get_data(as_text=True))

    def test_modifyRule(self):
        rid = 0
        response = self.client.post('http://localhost:5000/api/promotions/1/rules', data=json.dumps({
            'mode': 1,
            'requirement': 100,
            'discount': 10
        }))
        self.assertTrue('Login required.' in response.get_data(as_text=True))

        # print(response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/busers/session', data=json.dumps({
            "username": "manager",
            "password": "123",
        }))
        self.assertTrue("Successfully login." in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/promotions/1/rules', data=json.dumps({
            'mode': 1,
            'requirement': 100,
            'discount': 10
        }))
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        rid = data.get('id')
        self.assertTrue(200 == response.status_code)

        response = self.client.put('http://localhost:5000/api/promotions/1/rules/%d' % rid, data=json.dumps({
            'mode': 2,
            'requirement': 666,
            'discount': 6
        }))
        self.assertTrue('666' in response.get_data(as_text=True))

        response = self.client.put('http://localhost:5000/api/promotions/1/rules/%d' % (rid + 1), data=json.dumps({
            'mode': 2,
            'requirement': 666,
            'discount': 6
        }))
        self.assertTrue('rule not found' in response.get_data(as_text=True))

        response = self.client.get('http://localhost:5000/api/promotions/1/rules/%d' % rid)
        # print(response.get_data(as_text=True))
        self.assertTrue('666.0' in response.get_data(as_text=True))

        response = self.client.put('http://localhost:5000/api/busers/session')
        self.assertTrue('Successfully logout.' in response.get_data(as_text=True))



