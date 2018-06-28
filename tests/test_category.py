import unittest
from app import create_app, db
import json
import test_data

class FlaskClientTest(unittest.TestCase):

    menu = test_data.menu
    dishes = test_data.dishes
    category = test_data.category
    login = False
    create_menu = False
    # menuid = 100

    def setUp(self):
        self.app = create_app('Test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        # self.register_and_login()

        response = self.client.post('http://localhost:5000/api/busers/session', data=json.dumps({
            "username": "manager",
            "password": "123"
        }))
        # self.assertTrue("Successfully login." in response.get_data(as_text=True))

        self.login = True

        
        # if not self.create_menu:
        #     createFullMenu()
        #     self.create_menu = True

    def tearDown(self):
        # self.logout()
        response = self.client.put('http://localhost:5000/api/busers/session')
        self.assertTrue('Successfully logout.' in response.get_data(as_text=True))
        self.login = False

        db.session.remove()
        # db.drop_all()
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
    
    # 新增1个菜单, 2个类别, 4个菜品
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
        response = self.client.post('http://localhost:5000/api/busers/session', data=json.dumps({
            "username": "manager",
            "password": "123",
        }))
        # print(response.get_data(as_text=True))

        self.assertTrue("Successfully login." in response.get_data(as_text=True))

    # 注销登陆的manager账号
    def logout(self):
        response = self.client.put('http://localhost:5000/api/busers/session')
        self.assertTrue('Successfully logout.' in response.get_data(as_text=True))

    # 测试新建类别
    def test_newCategory(self):
        # 新建菜单
        id = self.createMenu()

        # 新建2个类别
        url = 'http://localhost:5000/api/menus/' + str(id) + '/categories/'
        response = self.client.post(url,
                        data=json.dumps(self.category))

        # print(response.get_data(as_text=True))
        self.assertTrue(200==response.status_code)

        self.category['name'] = '素菜'
        self.category['rank'] = 2
        url = 'http://localhost:5000/api/menus/' + str(id) + '/categories/'
        response = self.client.post(url,
                        data=json.dumps(self.category))
        # print(response.get_data(as_text=True))
        self.assertTrue(200==response.status_code)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        catid = data.get('id')

        # 获取菜单
        url = 'http://localhost:5000/api/menus/' + str(id)
        response = self.client.get(url)
        self.assertTrue(200==response.status_code)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        self.assertTrue(id==data.get('id'))
        content = data.get('content', None)
        self.assertTrue(content is not None)
        found = False
        for cat in content:
            if cat.get('id') == catid:
                found = True
                break
        self.assertTrue(found is True)
        # print(data)

    # 测试修改菜单
    def test_modifyCategory(self):

        # 新建一个菜单并获取id
        menuid = self.createMenu()

        # 新建1个类别
        url = 'http://localhost:5000/api/menus/' + str(menuid) + '/categories/'
        response = self.client.post(url,
                        data=json.dumps(self.category))
        self.assertTrue(200==response.status_code)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        catid = data.get('id')

        # 根据id修改类别
        url = 'http://localhost:5000/api/menus/' \
                + str(menuid) + '/categories/' + str(catid)
        response = self.client.put(url,
                        data=json.dumps({'name': '改个名'}))
        self.assertTrue(200==response.status_code)

        # 根据id获取菜单, 验证category name已改为'改个名'
        url = 'http://localhost:5000/api/menus/' + str(menuid)
        response = self.client.get(url)
        self.assertTrue(200==response.status_code)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        content = data.get('content', None)
        for cat in content:
            if cat.get('id') == catid:
                new_name = cat.get('name')
        self.assertTrue(new_name == '改个名')
        # print(data)

    # 测试删除类别
    def test_deleteCategory(self):

        # 新建菜单
        menuid = self.createMenu()

        # 新建1个类别
        url = 'http://localhost:5000/api/menus/' + str(menuid) + '/categories/'
        response = self.client.post(url,
                        data=json.dumps(self.category))
        self.assertTrue(200==response.status_code)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        catid = data.get('id')

        # 测试此时有1个category
        url = 'http://localhost:5000/api/menus/' + str(menuid)
        response = self.client.get(url)
        self.assertTrue(200==response.status_code)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        content = data.get('content', None)
        self.assertTrue(len(content) == 1)

        # 删除类别
        url = 'http://localhost:5000/api/menus/' \
                + str(menuid) + '/categories/' + str(catid)
        response = self.client.delete(url)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        print(data)
        self.assertTrue(200==response.status_code)

        # 测试没有了该类别
        url = 'http://localhost:5000/api/menus/' + str(menuid)
        response = self.client.get(url)
        self.assertTrue(200==response.status_code)
        data = response.get_data()
        data.decode('utf-8')
        data = json.loads(data)
        content = data.get('content', None)
        self.assertTrue(len(content) == 0)

        url = 'http://localhost:5000/api/menus/' \
                + str(menuid) + '/categories/' + str(catid)
        response = self.client.delete(url)
        self.assertTrue(404==response.status_code)
