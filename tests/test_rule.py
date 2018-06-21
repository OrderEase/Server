import unittest
from app import create_app, db

class FlaskClientTest(unittest.TestCase):

    promotions = [
    {
        "theme": "端午节活动",
        "begin": "2017-11-23 16:10:10",
        "end": "2017-11-23 16:10:10",
        "isend": 1
    },
    {
        "theme": "dfsfs端午节活动",
        "begin": "2017-06-11 5:10:10",
        "end": "2017-07-01 12:10:10",
        "isend": 2
    }]

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        response = self.client.post('http://localhost:5000/api/busers/', data={
            "username": "aaa",
            "password": "123",
            "authority": "manager"})
        self.assertTrue(response.status_code == 200)
        response = self.client.post('http://localhost:5000/api/busers/session', data={
            "username": "aaa",
            "password": "123",
        })
        self.assertTrue("Successfully login." in response.get_data(as_text=True))

        # 添加一条 rule 用于测试
        for promotion in self.promotions:
            response = self.client.post('http://localhost:5000/api/promotions/', data=promotion)
            # print(response.get_data(as_text=True))
            self.assertTrue(response.status_code == 200)

        response = self.client.post('http://localhost:5000/api/promotions/1/rules',
                data={
                'mode': 1,
                'requirement': 100,
                'discount': 10
                })
        self.assertTrue(200 == response.status_code)

        response = self.client.put('http://localhost:5000/api/busers/session')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_addRule(self):
        response = self.client.post('http://localhost:5000/api/promotions/1/rules', data={
            'mode': 1,
            'requirement': 100,
            'discount': 10
        })
        self.assertTrue('Login required.' in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/busers/session', data={
            "username": "aaa",
            "password": "123",
        })
        self.assertTrue("Successfully login." in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/promotions/1/rules',
                data={
                'mode': 3,
                'requirement': 100,
                'discount': 10
                })
        self.assertTrue('Mode is required to be 1 or 2.' in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/promotions/1/rules',
                data={
                'mode': 2,
                'requirement': -10,
                'discount': 10
                })
        self.assertTrue('Requirement is required and not negative.' in response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/promotions/1/rules',
                data={
                'mode': 2,
                'requirement': 100,
                'discount': -10
                })
        self.assertTrue('Discount is required and not negative.' in response.get_data(as_text=True))

    def test_getRule(self):
        response = self.client.post('http://localhost:5000/api/promotions/1/rules', data={
            'mode': 1,
            'requirement': 100,
            'discount': 10
        })
        self.assertTrue('Login required.' in response.get_data(as_text=True))

        # print(response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/busers/session', data={
            "username": "aaa",
            "password": "123",
        })
        self.assertTrue("Successfully login." in response.get_data(as_text=True))

        response = self.client.get('http://localhost:5000/api/promotions/1/rules/1')
        # print(response.get_data(as_text=True))
        self.assertTrue('{"id": 1, "mode": 1, "requirement": 100.0, "discount": 10.0}' in response.get_data(as_text=True))

        response = self.client.get('http://localhost:5000/api/promotions/1/rules/2')
        # print(response.get_data(as_text=True))
        self.assertTrue('rule not found' in response.get_data(as_text=True))

    def test_modifyRule(self):
        response = self.client.post('http://localhost:5000/api/promotions/1/rules', data={
            'mode': 1,
            'requirement': 100,
            'discount': 10
        })
        self.assertTrue('Login required.' in response.get_data(as_text=True))

        # print(response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/busers/session', data={
            "username": "aaa",
            "password": "123",
        })
        self.assertTrue("Successfully login." in response.get_data(as_text=True))

        response = self.client.put('http://localhost:5000/api/promotions/1/rules/1',
                data={
                'mode': 2,
                'requirement': 666,
                'discount': 6
                })
        self.assertTrue('{"id": 1, "mode": 2, "requirement": 666.0, "discount": 6.0}' in response.get_data(as_text=True))

        response = self.client.put('http://localhost:5000/api/promotions/1/rules/2',
                data={
                'mode': 2,
                'requirement': 666,
                'discount': 6
                })
        self.assertTrue('rule not found' in response.get_data(as_text=True))

        response = self.client.get('http://localhost:5000/api/promotions/1/rules/1')
        # print(response.get_data(as_text=True))
        self.assertTrue('{"id": 1, "mode": 2, "requirement": 666.0, "discount": 6.0}' in response.get_data(as_text=True))

    def test_deleteRule(self):
        response = self.client.post('http://localhost:5000/api/promotions/1/rules', data={
            'mode': 1,
            'requirement': 100,
            'discount': 10
        })
        self.assertTrue('Login required.' in response.get_data(as_text=True))

        # print(response.get_data(as_text=True))

        response = self.client.post('http://localhost:5000/api/busers/session', data={
            "username": "aaa",
            "password": "123",
        })
        self.assertTrue("Successfully login." in response.get_data(as_text=True))

        response = self.client.delete('http://localhost:5000/api/promotions/1/rules/1')
        self.assertTrue(200 == response.status_code)

        response = self.client.delete('http://localhost:5000/api/promotions/1/rules/1')
        self.assertTrue('rule not found' in response.get_data(as_text=True))

