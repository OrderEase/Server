# import unittest
# from app import create_app, db
# import json
# import test_data

# class FlaskClientTest(unittest.TestCase):

#     menu = test_data.menu
#     dishes = test_data.dishes
#     category = test_data.category

#     def setUp(self):
#         self.app = create_app('Test')
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#         db.create_all()
#         self.client = self.app.test_client()

#         self.register_and_login()

#     def tearDown(self):
#         self.logout()
#         db.session.remove()
#         # db.drop_all()
#         self.app_context.pop()

#     # 新建菜单, 使用self.menu
#     def createMenu(self):
#         response = self.client.post('http://localhost:5000/api/menus/',
#                         data=json.dumps(self.menu))
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         return data.get('id')

#     # 注册一个manager账号并登陆
#     def register_and_login(self):
#         response = self.client.post('http://localhost:5000/api/busers/session', data=json.dumps({
#             "username": "manager",
#             "password": "123",
#         }))

#         self.assertTrue("Successfully login." in response.get_data(as_text=True))

#     # 注销登陆的manager账号
#     def logout(self):
#         response = self.client.put('http://localhost:5000/api/busers/session')
#         self.assertTrue('Successfully logout.' in response.get_data(as_text=True))

#     # 新增1个菜单, 2个类别, 4个菜品
#     def createFullMenu(self):
#         menuid = self.createMenu()

#         # 新建2个类别
#         url = 'http://localhost:5000/api/menus/' + str(menuid) + '/categories/'
#         response = self.client.post(url,
#                         data=json.dumps(self.category))
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         catid1 = data.get('id')

#         self.category['name'] = '素菜'
#         self.category['rank'] = 2
#         response = self.client.post(url,
#                         data=json.dumps(self.category))
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         catid2 = data.get('id')

#         # 新建4个菜品
#         url = 'http://localhost:5000/api/menus/' \
#                 + str(menuid) + '/categories/' + str(catid2) + '/dishes/'
#         response = self.client.post(url,
#                         data=json.dumps(self.dishes[0]))
#         self.assertTrue(200==response.status_code)
#         response = self.client.post(url,
#                         data=json.dumps(self.dishes[1]))
#         self.assertTrue(200==response.status_code)

#         url = 'http://localhost:5000/api/menus/' \
#                 + str(menuid) + '/categories/' + str(catid1) + '/dishes/'
#         response = self.client.post(url,
#                         data=json.dumps(self.dishes[2]))
#         self.assertTrue(200==response.status_code)
#         response = self.client.post(url,
#                         data=json.dumps(self.dishes[3]))
#         self.assertTrue(200==response.status_code)

#         return menuid

#     # 测试新建菜品
#     def test_newDish(self):
#         # 新建菜单
#         menuid = self.createMenu()

#         # 新建1个类别
#         url = 'http://localhost:5000/api/menus/' + str(menuid) + '/categories/'
#         response = self.client.post(url,
#                         data=json.dumps(self.category))
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         catid = data.get('id')

#         # 新建一个菜品
#         url = 'http://localhost:5000/api/menus/' \
#                 + str(menuid) + '/categories/' + str(catid) + '/dishes/'
#         response = self.client.post(url,
#                         data=json.dumps(self.dishes[0]))
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         dishid = data.get('id')

#         # 验证菜品成功增加
#         url = 'http://localhost:5000/api/menus/' + str(menuid)
#         response = self.client.get(url)
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         content = data.get('content', None)
#         dishes = content[0].get('dishes')
#         self.assertTrue(dishes[0].get('id') == dishid)

#     # 测试修改菜品
#     def test_modifyDish(self):

#         # 新建一个完整菜单并获取id
#         menuid = self.createFullMenu()

#         # 根据id获取菜单, 获取第一个类别id，和第一个菜id
#         url = 'http://localhost:5000/api/menus/' + str(menuid)
#         response = self.client.get(url)
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         content = data.get('content', None)
#         catid = content[0].get('id')
#         dishes = content[0].get('dishes')
#         dishid = dishes[0].get('id')

#         # 根据id修改菜品
#         url = 'http://localhost:5000/api/menus/' \
#                 + str(menuid) + '/categories/' + str(catid) \
#                 + '/dishes/' + str(dishid)
#         response = self.client.put(url,
#                         data=json.dumps({'name': '白灼许琦'}))
#         self.assertTrue(200==response.status_code)

#         # 根据id获取菜品, 验证dish name已改为'白灼许琦'
#         url = 'http://localhost:5000/api/menus/' \
#                 + str(menuid) + '/categories/' + str(catid) \
#                 + '/dishes/' + str(dishid)
#         response = self.client.get(url)
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         self.assertTrue(data.get('name') == '白灼许琦')
#         # print(data)

#     # 测试获取菜品
#     def test_getDish(self):

#         # 新建一个完整菜单并获取id
#         menuid = self.createFullMenu()

#         # 根据id获取菜单, 获取第一个类别id，和第一个菜id
#         url = 'http://localhost:5000/api/menus/' + str(menuid)
#         response = self.client.get(url)
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         content = data.get('content', None)
#         catid = content[0].get('id')
#         dishes = content[0].get('dishes')
#         dishid = dishes[0].get('id')

#         # 根据id获取菜品
#         url = 'http://localhost:5000/api/menus/' \
#                 + str(menuid) + '/categories/' + str(catid) \
#                 + '/dishes/' + str(dishid)
#         response = self.client.get(url)
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         self.assertTrue(data.get('id') == dishid)
#         # print(data)

#     # 测试删除菜品
#     def test_deleteDish(self):

#         # 新建一个完整菜单并获取id
#         menuid = self.createFullMenu()

#         # 根据id获取菜单, 获取第一个类别id，和第一个菜id
#         url = 'http://localhost:5000/api/menus/' + str(menuid)
#         response = self.client.get(url)
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         content = data.get('content', None)
#         catid = content[0].get('id')
#         dishes = content[0].get('dishes')
#         dishid = dishes[0].get('id')

#         # 根据id获取菜品
#         url = 'http://localhost:5000/api/menus/' \
#                 + str(menuid) + '/categories/' + str(catid) \
#                 + '/dishes/' + str(dishid)
#         response = self.client.get(url)
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         self.assertTrue(data.get('id') == dishid)

#         # 根据id删除菜品
#         url = 'http://localhost:5000/api/menus/' \
#                 + str(menuid) + '/categories/' + str(catid) \
#                 + '/dishes/' + str(dishid)
#         response = self.client.delete(url)
#         self.assertTrue(200==response.status_code)

#         # 根据id获取菜品会404
#         url = 'http://localhost:5000/api/menus/' \
#                 + str(menuid) + '/categories/' + str(catid) \
#                 + '/dishes/' + str(dishid)
#         response = self.client.get(url)
#         self.assertTrue(404==response.status_code)

#         # 菜单中也没有了这个菜
#         url = 'http://localhost:5000/api/menus/' + str(menuid)
#         response = self.client.get(url)
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         content = data.get('content', None)
#         found = False
#         for cat in content:
#             dishes = cat.get('dishes')
#             for dish in dishes:
#                 if dish.get('id') == dishid:
#                     found = True
#         self.assertFalse(found)

#     # 测试获取用户菜单
#     def test_getAvaliableDishes(self):
#         # 新建一个完整菜单并获取id
#         menuid = self.createFullMenu()

#         # 根据id获取菜单, 获取第一个类别id，和第二个类别第一个菜id
#         url = 'http://localhost:5000/api/menus/' + str(menuid)
#         response = self.client.get(url)
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         content = data.get('content', None)
#         self.assertTrue(content is not None)
#         catid1 = content[0].get('id')
#         catid2 = content[1].get('id')
#         dishes = content[1].get('dishes')
#         dishid = dishes[0].get('id')

#         # 删除第一个类别和第二个类别的第一个菜
#         url = 'http://localhost:5000/api/menus/' \
#              + str(menuid) + '/categories/' + str(catid1)
#         response = self.client.delete(url)
#         self.assertTrue(200==response.status_code)

#         url = 'http://localhost:5000/api/menus/' \
#                 + str(menuid) + '/categories/' + str(catid2) \
#                 + '/dishes/' + str(dishid)
#         response= self.client.put(url, data=json.dumps({'avaliable': 0}))

#         # 获取菜单
#         url = 'http://localhost:5000/api/menus/cuser'
#         response = self.client.get(url)
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         print(data)