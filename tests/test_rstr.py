import unittest
from app import create_app, db

class FlaskClientTest(unittest.TestCase):

    myorder1 = {
    "tableId": "23E",
    "dishes": "1, 2"
    }
    myorder2 = {
    "tableId": "23E",
    "dishes": "3, 2"
    }
    dishes = [{
    "name": "毛血旺",
    "category": "荤菜",
    "price": 28.5,
    "stock": 99,
    "avaliable": 1,
    "likes": 4,
    "description": "Hello 毛血旺",
    "img": "https://raw.githubusercontent.com/OrderEase/Server/master/assets/maoxuewan.jpg"
    },{
    "name": "西红柿炒番茄",
    "category": "素菜",
    "price": 12.5,
    "stock": 99,
    "avaliable": 1,
    "likes": 6,
    "description": "很难吃",
    "img": "https://raw.githubusercontent.com/OrderEase/Server/master/assets/tomato.jpg"
    },{
    "name": "马铃薯炒土豆",
    "category": "素菜",
    "price": 8.5,
    "stock": 99,
    "avaliable": 1,
    "likes": 5,
    "description": "很好吃",
    "img": "https://raw.githubusercontent.com/OrderEase/Server/master/assets/potato.jpg"
    },{
    "name": "红烧许琦",
    "category": "荤菜",
    "price": 128.5,
    "stock": 99,
    "avaliable": 1,
    "likes": 100,
    "description": "哈哈"
    }]

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        response = self.client.post('http://localhost:5000/api/buser/', data={
            "restId": 1,
            "username": "aaa",
            "role": "BUSINESS",
            "password": "123",
            "authority": "MANAGER"})
        self.assertTrue(response.status_code == 200)
        response = self.client.post('http://localhost:5000/api/buser/session', data={
            "username": "aaa",
            "restId": 1,
            "password": "123",
            "role": "BUSINESS"
        })
        self.assertTrue("Successfully login." in response.get_data(as_text=True))

        # self.buser_id = response.json['buser_id']

        for dish in self.dishes:
            response = self.client.post('http://localhost:5000/api/dish/', data=dish)
            self.assertTrue(200 == response.status_code)

    def tearDown(self):
        response = self.client.put('http://localhost:5000/api/buser/session')
        self.assertTrue('Successfully logout.' in response.get_data(as_text=True))

        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_modifyRstr(self):
        response = self.client.put('http://localhost:5000/api/rstr/buid/1',
                data={
                'name':'点都德',
                'info': '茶楼'
                })
        # print(response.status_code)
        self.assertTrue(200 == response.status_code)

    def test_postMenu(self):
        response = self.client.put('http://localhost:5000/api/rstr/buid/1',
                                    data={
                                    'name':'点都德',
                                    'info': '茶楼'
                                    })
        self.assertTrue(200 == response.status_code)

        response = self.client.post('http://localhost:5000/api/rstr/buid/1/menu',
                                    data={
                                    'name':'春季菜单',
                                    'dishes':'1,2,3,4'
                                    })
        self.assertTrue(200 == response.status_code)

    def test_putMenu(self):
        response = self.client.put('http://localhost:5000/api/rstr/buid/1',
                                    data={
                                    'name':'点都德',
                                    'info': '茶楼'
                                    })
        self.assertTrue(200 == response.status_code)

        response = self.client.post('http://localhost:5000/api/rstr/buid/1/menu',
                                    data={
                                    'name':'春季菜单',
                                    'dishes':'1,2,3,4'
                                    })
        self.assertTrue(200 == response.status_code)

        response = self.client.put('http://localhost:5000/api/rstr/buid/1/menu/1',
                                    data={
                                    'name':'夏季菜单',
                                    'dishes':'1,2'
                                    })
        self.assertTrue(200 == response.status_code)

    def test_getRstr(self):
        response = self.client.put('http://localhost:5000/api/rstr/buid/1',
                                    data={
                                    'name':'点都德',
                                    'info': '茶楼'
                                    })
        self.assertTrue(200 == response.status_code)

        response = self.client.post('http://localhost:5000/api/rstr/buid/1/menu',
                                    data={
                                    'name':'春季菜单',
                                    'dishes':'1,2,3,4'
                                    })
        self.assertTrue(200 == response.status_code)

        response = self.client.get('http://localhost:5000/api/rstr/')
        self.assertTrue(200 == response.status_code)

