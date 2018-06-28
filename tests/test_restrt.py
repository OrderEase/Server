import unittest
from app import create_app, db
import json
import test_data
import app.gen_data as data_generator

class FlaskClientTest(unittest.TestCase):

    menu = test_data.menu
    dishes = test_data.dishes
    category = test_data.category
    login = False

    def setUp(self):
        self.app = create_app('Test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        data_generator.gen_basic_data()

        # self.register_and_login()
        response = self.client.post('http://localhost:5000/api/busers/session', data=json.dumps({
            "username": "manager",
            "password": "123"
        }))
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        # print(data)
        # self.assertTrue("Successfully login." in response.get_data(as_text=True))

        self.login = True

    def tearDown(self):
        # self.logout()
        response = self.client.put('http://localhost:5000/api/busers/session')
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        # print(data)
        # self.assertTrue('Successfully logout.' in response.get_data(as_text=True))
        self.login = False
        data_generator.remove_data()
        db.session.remove()
        self.app_context.pop()

    # 新建菜单, 使用self.menu
    # 新增1个菜单, 2个类别, 4个菜品
    def createMenu(self):
        response = self.client.post('http://localhost:5000/api/menus/',
                        data=json.dumps(self.menu))
        self.assertTrue(200==response.status_code)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        return data.get('id')

    def createFullMenu(self):
        menuid = self.createMenu()

        # 新建2个类别
        url = 'http://localhost:5000/api/menus/' + str(menuid) + '/categories/'
        response = self.client.post(url,
                        data=json.dumps(self.category))
        self.assertTrue(200==response.status_code)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        catid1 = data.get('id')

        self.category['name'] = '素菜'
        self.category['rank'] = 2
        response = self.client.post(url,
                        data=json.dumps(self.category))
        self.assertTrue(200==response.status_code)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        catid2 = data.get('id')

        # 新建4个菜品
        url = 'http://localhost:5000/api/menus/' \
                + str(menuid) + '/categories/' + str(catid2) + '/dishes/'
        response = self.client.post(url,
                        data=json.dumps(self.dishes[0]))
        self.assertTrue(200==response.status_code)
        response = self.client.post(url,
                        data=json.dumps(self.dishes[1]))
        self.assertTrue(200==response.status_code)

        url = 'http://localhost:5000/api/menus/' \
                + str(menuid) + '/categories/' + str(catid1) + '/dishes/'
        response = self.client.post(url,
                        data=json.dumps(self.dishes[2]))
        self.assertTrue(200==response.status_code)
        response = self.client.post(url,
                        data=json.dumps(self.dishes[3]))
        self.assertTrue(200==response.status_code)

        return menuid

    # 注册一个manager账号并登陆
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

    # 注销登陆的manager账号
    def logout(self):
        response = self.client.put('http://localhost:5000/api/busers/session')
        self.assertTrue('Successfully logout.' in response.get_data(as_text=True))

    # 测试获取餐馆信息
    def test_getRestrt(self):
        # 新建菜单
        id = self.createFullMenu()

        response = self.client.get('http://localhost:5000/api/restrt/')
        self.assertTrue(200==response.status_code)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        self.assertTrue(1==data.get('id'))

    # 测试修改餐馆
    def test_modifyRestr(self):

        # 新建菜单
        id = self.createFullMenu()

        response = self.client.put('http://localhost:5000/api/restrt/',
                    data=json.dumps({'open':'08:00',
                          'close': '22:00'}))
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        # print(data)
        self.assertTrue(200==response.status_code)

        response = self.client.get('http://localhost:5000/api/restrt/')
        self.assertTrue(200==response.status_code)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        self.assertTrue(1==data.get('id'))
        # print(data)
