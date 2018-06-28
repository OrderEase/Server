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
        self.assertTrue("Successfully login." in response.get_data(as_text=True))

        self.login = True

    def tearDown(self):
        # self.logout()
        response = self.client.put('http://localhost:5000/api/busers/session')
        self.assertTrue('Successfully logout.' in response.get_data(as_text=True))
        self.login = False
        data_generator.remove_data()
        db.session.remove()
        self.app_context.pop()

    # 新建菜单, 使用self.menu
    def createMenu(self):
        response = self.client.post('http://localhost:5000/api/menus/',
                        data=json.dumps(self.menu))
        self.assertTrue(200==response.status_code)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        return data.get('id')

    # 注册一个manager账号并登陆
    def register_and_login(self):
        response = self.client.post('http://localhost:5000/api/busers/session', data=json.dumps({
            "username": "manager",
            "password": "123",
        }))

        self.assertTrue("Successfully login." in response.get_data(as_text=True))

    # 注销登陆的manager账号
    def logout(self):
        response = self.client.put('http://localhost:5000/api/busers/session')
        self.assertTrue('Successfully logout.' in response.get_data(as_text=True))

    # 测试新建菜单
    def test_newMenu(self):
        response = self.client.post('http://localhost:5000/api/menus/',
                        data=json.dumps(self.menu))
        self.assertTrue(200==response.status_code)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        # print(data)

    # 测试获取所有菜单
    def test_getAllMenu(self):

        # 新建2个菜单
        self.createMenu()
        self.menu['name'] = '夏季菜单'
        self.createMenu()

        # 获取所有菜单
        response = self.client.get('http://localhost:5000/api/menus/')
        self.assertTrue(200==response.status_code)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        # print(data)

    # 测试根据id获取
    def test_getMenuById(self):

        # 新建一个菜单并获取id
        id = self.createMenu()

        # 用id获取菜单
        url = 'http://localhost:5000/api/menus/' + str(id)
        response = self.client.get(url)
        self.assertTrue(200==response.status_code)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        self.assertTrue(id==data.get('id'))
        # print(data)

    # 测试修改菜单
    def test_modifyMenu(self):

        # 新建一个菜单并获取id
        id = self.createMenu()

        url = 'http://localhost:5000/api/menus/' + str(id)

        # 验证能获取菜单，且菜单名不等于'改个名'
        response = self.client.get(url)
        self.assertTrue(200==response.status_code)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        self.assertTrue(self.menu['name']==data.get('name'))
        self.assertFalse(self.menu['name']=='改个名')

        # 根据id修改菜单
        response = self.client.put(url,
                        data=json.dumps({'name': '改个名'}))
        self.assertTrue(200==response.status_code)

        # 根据id获取菜单, 验证name已改为'改个名'
        response = self.client.get(url)
        self.assertTrue(200==response.status_code)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        self.assertTrue('改个名'==data.get('name'))
        # print(data)

    # 测试删除菜单
    def test_deleteMenu(self):

        # 新建一个菜单并获取id
        id = self.createMenu()

        url = 'http://localhost:5000/api/menus/' + str(id)

        # 验证能获取菜单
        response = self.client.get(url)
        self.assertTrue(200==response.status_code)

        # 删除菜单
        response = self.client.delete(url)
        self.assertTrue(200==response.status_code)

        # 验证不能获取菜单
        response = self.client.get(url)
        self.assertTrue(404==response.status_code)

        # response = self.client.get('http://localhost:5000/api/menus/')
        # self.assertTrue(200==response.status_code)
        # data = response.get_data()
        # data.decode('utf-8')
        # data = json.loads(data)
        # self.assertTrue(data.get('menus')==[])
        # # print(data)

