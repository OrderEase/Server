# import unittest
# from app import create_app, db
# import json
# import test_data

# class FlaskClientTest(unittest.TestCase):

#     menu = test_data.menu
#     dishes = test_data.dishes
#     category = test_data.category

#     def setUp(self):
#         self.app = create_app()
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#         db.create_all()
#         self.client = self.app.test_client()

#         self.register_and_login()

#     def tearDown(self):
#         self.logout()
#         # db.session.remove()
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
#         response = self.client.post('http://localhost:5000/api/busers/', data={
#             "username": "aaa",
#             "password": "123",
#             "authority": "manager"})

#         self.assertTrue(response.status_code == 200)

#         response = self.client.post('http://localhost:5000/api/busers/session', data={
#             "username": "aaa",
#             "password": "123",
#         })

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
#         response = self.client.post(url, data=json.dumps(self.category))
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         catid1 = data.get('id')

#         self.category['name'] = '素菜'
#         self.category['rank'] = 2
#         response = self.client.post(url, data=json.dumps(self.category))
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         catid2 = data.get('id')

#         dishids = []
#         # 新建4个菜品
#         url = 'http://localhost:5000/api/menus/' \
#                 + str(menuid) + '/categories/' + str(catid2) + '/dishes/'
#         response = self.client.post(url,
#                         data=json.dumps(self.dishes[0]))
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         dishids.append(data.get('id'))
#         response = self.client.post(url,
#                         data=json.dumps(self.dishes[1]))
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         dishids.append(data.get('id'))

#         url = 'http://localhost:5000/api/menus/' \
#                 + str(menuid) + '/categories/' + str(catid1) + '/dishes/'
#         response = self.client.post(url,
#                         data=json.dumps(self.dishes[2]))
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         dishids.append(data.get('id'))
#         response = self.client.post(url,
#                         data=json.dumps(self.dishes[3]))
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         dishids.append(data.get('id'))

#         return dishids

#     def createOrders(self):
#         # 新建4个菜
#         dishids = self.createFullMenu()

#         orders = [{
#             'tableId': '23E',
#             "total": 315,
#             "due": 315,
#             "content": [
#                     {
#                         "dish": dishids[0],
#                         "quantity": 1
#                     },
#                     {
#                         "dish": dishids[1],
#                         "quantity": 2
#                     },
#                     {
#                         "dish": dishids[2],
#                         "quantity": 1
#                     },
#                     {
#                         "dish": dishids[3],
#                         "quantity": 2
#                     }
#                 ]
#             },
#             {
#                 'tableId': '26A',
#                 "total": 186.5,
#                 "due": 186.5,
#                 "content": [
#                     {
#                         "dish": dishids[0],
#                         "quantity": 1
#                     },
#                     {
#                         "dish": dishids[1],
#                         "quantity": 2
#                     },
#                     {
#                         "dish": dishids[2],
#                         "quantity": 1
#                     },
#                     {
#                         "dish": dishids[3],
#                         "quantity": 1
#                     }
#                 ]
#             }
#         ]
#         # 新建订单1
#         order = orders[0]
#         url = 'http://localhost:5000/api/orders/cuser/'
#         response = self.client.post(url, data=json.dumps(order))
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         id1 = data.get('id')
#         self.assertTrue(id1 is not None)
#         self.assertTrue(200==response.status_code)

#         # 新建订单2
#         order = orders[1]
#         response = self.client.post(url, data=json.dumps(order))
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         id2 = data.get('id')
#         self.assertTrue(id2 is not None)
#         self.assertTrue(200==response.status_code)

#         return id1, id2, dishids

#     # 测试新建订单
#     def test_newOrder(self):
#         # 新建4个菜
#         dishids = self.createFullMenu()

#         order = {
#             'tableId': '23E',
#             "total": 315,
#             "due": 315,
#             "content": [
#                     {
#                         "dish": dishids[0],
#                         "quantity": 1
#                     },
#                     {
#                         "dish": dishids[1],
#                         "quantity": 2
#                     },
#                     {
#                         "dish": dishids[2],
#                         "quantity": 1
#                     },
#                     {
#                         "dish": dishids[3],
#                         "quantity": 2
#                     }
#                 ]
#             }

#         # 新建订单
#         url = 'http://localhost:5000/api/orders/cuser/'
#         response = self.client.post(url, data=json.dumps(order))
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         # print(data)
#         self.assertTrue(200==response.status_code)

#     # 测试获取全部订单
#     def test_getAllOrdersC(self):
#         # 新建2个订单
#         id1, id2, dishids = self.createOrders()

#         # 测试获取全部菜单
#         url = 'http://localhost:5000/api/orders/cuser/'
#         response = self.client.get(url)
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         orders = data.get('orders')
#         found1 = found2 = False
#         for o in orders:
#             id = o.get('id')
#             if id == id1:
#                 found1 = True
#             if id == id2:
#                 found2 = True
#         self.assertTrue(found1)
#         self.assertTrue(found2)

#     # 测试付款
#     def test_payOrder(self):
#         # 新建2个订单
#         id1, id2, dishids = self.createOrders()

#         # 测试付款
#         url = 'http://localhost:5000/api/orders/cuser/oid/' + str(id1)
#         response = self.client.post(url,
#                         data=json.dumps({'payId':123}))
#         self.assertTrue(200==response.status_code)

#         # 测试获取订单并显示已付款
#         url = 'http://localhost:5000/api/orders/cuser/oid/' + str(id1)
#         response = self.client.get(url)
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         self.assertTrue(data.get('isPay') == 1)

#     # 测试用户修改订单(修改催单, 点赞)
#     def test_modifyOrderC(self):
#         # 新建2个订单
#         id1, id2, dishids = self.createOrders()

#         # 测试付款
#         url = 'http://localhost:5000/api/orders/cuser/oid/' + str(id1)
#         response = self.client.post(url,
#                         data=json.dumps({'payId':123}))
#         self.assertTrue(200==response.status_code)

#         # 测试催单和点赞
#         url = 'http://localhost:5000/api/orders/cuser/oid/' + str(id1)
#         tmp = {
#             'dishId': dishids[0],
#             'like': 1,
#             'urge': 1
#         }
#         response = self.client.put(url, data=json.dumps(tmp))
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         # print(data)
#         self.assertTrue(200==response.status_code)

#         # 获取订单检查修改内容
#         url = 'http://localhost:5000/api/orders/cuser/oid/' + str(id1)
#         response = self.client.get(url)
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         ois = data.get('orderItems')
#         self.assertTrue(ois is not None)
#         for item in ois:
#             if item.get('dishId') == dishids[0]:
#                 self.assertTrue(item.get('like') == 1)
#                 self.assertTrue(item.get('urge') == 1)
#                 break

#     # 测试商家修改订单(修改完成, 完成时间)
#     def test_modifyOrderB(self):
#         # 新建2个订单
#         id1, id2, dishids = self.createOrders()

#         # 测试付款
#         url = 'http://localhost:5000/api/orders/cuser/oid/' + str(id1)
#         response = self.client.post(url,
#                         data=json.dumps({'payId':123}))
#         self.assertTrue(200==response.status_code)

#         # 测试修改完成和完成时间
#         url = 'http://localhost:5000/api/orders/buser/oid/' + str(id1)
#         tmp = {
#             'dishId': dishids[0],
#             'finished': 1,
#             'time': '2018-06-23 12:00:00'
#         }
#         response = self.client.put(url, data=json.dumps(tmp))
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         # print(data)
#         self.assertTrue(200==response.status_code)

#         # 获取订单检查修改内容
#         url = 'http://localhost:5000/api/orders/buser/oid/' + str(id1)
#         response = self.client.get(url)
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         ois = data.get('orderItems')
#         self.assertTrue(ois is not None)
#         for item in ois:
#             if item.get('dishId') == dishids[0]:
#                 # print(item)
#                 self.assertTrue(item.get('finished') == 1)
#                 self.assertTrue(item.get('time') == '2018-06-23 12:00:00')
#                 break

#         # 测试全部完成
#         url = 'http://localhost:5000/api/orders/buser/oid/' + str(id1)
#         for i in [1, 2, 3]:
#             tmp = {
#                 'dishId': dishids[i],
#                 'finished': 1,
#                 'time': '2018-06-23 12:00:00'
#             }
#             response = self.client.put(url, data=json.dumps(tmp))
#             self.assertTrue(200==response.status_code)

#         # 获取订单检查修改内容
#         url = 'http://localhost:5000/api/orders/buser/oid/' + str(id1)
#         response = self.client.get(url)
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         self.assertTrue(data.get('finished') == 1)

#     # 测试获取全部订单
#     def test_getAllOrdersB(self):
#         # 新建2个订单
#         id1, id2, dishids = self.createOrders()

#         # 测试获取全部菜单
#         url = 'http://localhost:5000/api/orders/buser/'
#         response = self.client.get(url)
#         self.assertTrue(200==response.status_code)
#         data = response.get_data()
#         data.decode('utf-8')
#         data = json.loads(data)
#         orders = data.get('orders')
#         found1 = found2 = False
#         for o in orders:
#             id = o.get('id')
#             if id == id1:
#                 found1 = True
#             if id == id2:
#                 found2 = True
#         self.assertTrue(found1)
#         self.assertTrue(found2)