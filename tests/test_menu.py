import unittest
from app import create_app, db
import json

class FlaskClientTest(unittest.TestCase):
    menu = {
        'name': '春季菜单',
        'used': 1
    }

    dishes = [{
        "name": "毛血旺",
        'rank': 1,
        "price": 28.5,
        "stock": 99,
        "avaliable": 1,
        "description": "Hello 毛血旺",
        "img": "https://raw.githubusercontent.com/OrderEase/Server/master/assets/maoxuewan.jpg"
    },{
        "name": "西红柿炒番茄",
        'rank': 2,
        "price": 12.5,
        "stock": 99,
        "avaliable": 1,
        "description": "很难吃",
        "img": "https://raw.githubusercontent.com/OrderEase/Server/master/assets/tomato.jpg"
    },{
        "name": "马铃薯炒土豆",
        'rank': 3,
        "price": 8.5,
        "stock": 99,
        "avaliable": 1,
        "description": "很好吃",
        "img": "https://raw.githubusercontent.com/OrderEase/Server/master/assets/potato.jpg"
    },{
        "name": "红烧许琦",
        'rank': 4,
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

        self.register_and_login()

    def tearDown(self):
        self.logout()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def createMenu(self):
        response = self.client.post('http://localhost:5000/api/menus/', 
                        data=self.menu)
        self.assertTrue(200==response.status_code)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        return data.get('id')

    def register_and_login(self):
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

    def logout(self):
        response = self.client.put('http://localhost:5000/api/busers/session')
        self.assertTrue('Successfully logout.' in response.get_data(as_text=True))

    def test_newMenu(self):
        response = self.client.post('http://localhost:5000/api/menus/', 
                        data=self.menu)
        self.assertTrue(200==response.status_code)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)

    def test_getAllMenu(self):
        self.createMenu()
        self.menu['name'] = '夏季菜单'
        self.createMenu()

        response = self.client.get('http://localhost:5000/api/menus/')
        # print(response.status_code)
        self.assertTrue(200==response.status_code)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        # print(data)
    
    def test_getMenuById(self):
        id = self.createMenu()

        url = 'http://localhost:5000/api/menus/' + str(id)
        response = self.client.get(url)
        # print(response.status_code)
        self.assertTrue(200==response.status_code)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        print(data)
