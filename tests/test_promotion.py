# import unittest
# from app import create_app, db

# class FlaskClientTest(unittest.TestCase):

#     promotions = [
#     {
#         "theme": "qqq",
#         "begin": "2017-11-23 16:10:10",
#         "end": "2017-11-23 16:10:10",
#         "isend": 1
#     },
#     {
#         "theme": "eee",
#         "begin": "2017-06-11 5:10:10",
#         "end": "2017-07-01 12:10:10",
#         "isend": 2
#     }]

#     def setUp(self):
#         self.app = create_app()
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#         db.create_all()
#         self.client = self.app.test_client()

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

#         for promotion in self.promotions:
#             response = self.client.post('http://localhost:5000/api/promotions/', data=promotion)
#             # print(response.get_data(as_text=True))
#             self.assertTrue(response.status_code == 200)

#         response = self.client.post('http://localhost:5000/api/promotions/1/rules', data={
#             'mode': 1,
#             'requirement': 100,
#             'discount': 10
#         })
#         # print(response.get_data(as_text=True))

#         # 退出
#         response = self.client.put('http://localhost:5000/api/busers/session')

#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#         self.app_context.pop()

#     def test_addPromotion(self):
#         response = self.client.post('http://localhost:5000/api/promotions/', data={
#             "theme": "端午节活动",
#             "begin": "2017-11-23 16:10:10",
#             "end": "2017-11-23 16:10:10",
#             "isend": 1
#         })
#         # print(response.get_data(as_text=True))
#         self.assertTrue('Login required.' in response.get_data(as_text=True))

#         response = self.client.post('http://localhost:5000/api/busers/session', data={
#             "username": "aaa",
#             "password": "123",
#         })
#         # print(response.get_data(as_text=True))
#         self.assertTrue("Successfully login." in response.get_data(as_text=True))

#         response = self.client.post('http://localhost:5000/api/promotions/', data={
#             "theme": "端午节活动",
#             "begin": "2017-11-23 16:10:10",
#             "end": "2017-11-23 16:10:10",
#             "isend": 1
#         })
#         # print(response.get_data(as_text=True))
#         self.assertTrue(response.status_code == 200)

#     def test_getPromotions(self):
#         response = self.client.post('http://localhost:5000/api/promotions/', data={
#             "theme": "端午节活动",
#             "begin": "2017-11-23 16:10:10",
#             "end": "2017-11-23 16:10:10",
#             "isend": 1
#         })
#         self.assertTrue('Login required.' in response.get_data(as_text=True))

#         response = self.client.post('http://localhost:5000/api/busers/session', data={
#             "username": "aaa",
#             "password": "123",
#         })
#         self.assertTrue("Successfully login." in response.get_data(as_text=True))

#         response = self.client.get('http://localhost:5000/api/promotions/')
#         self.assertTrue('[{"id": 1, "theme": "qqq", "begin": "2017-11-23 16:10:10", "end": "2017-11-23 16:10:10", "isend": 1, "rules": [{"id": 1, "mode": 1, "requirement": 100.0, "discount": 10.0}]}, {"id": 2, "theme": "eee", "begin": "2017-06-11 05:10:10", "end": "2017-07-01 12:10:10", "isend": 2, "rules": []}]' in response.get_data(as_text=True))
#         # print(response.get_data(as_text=True))

#     def test_getSinglePromotion(self):
#         response = self.client.post('http://localhost:5000/api/promotions/', data={
#             "theme": "端午节活动",
#             "begin": "2017-11-23 16:10:10",
#             "end": "2017-11-23 16:10:10",
#             "isend": 1
#         })
#         self.assertTrue('Login required.' in response.get_data(as_text=True))

#         response = self.client.post('http://localhost:5000/api/busers/session', data={
#             "username": "aaa",
#             "password": "123",
#         })
#         self.assertTrue("Successfully login." in response.get_data(as_text=True))

#         response = self.client.get('http://localhost:5000/api/promotions/1')
#         self.assertTrue('{"id": 1, "theme": "qqq", "begin": "2017-11-23 16:10:10", "end": "2017-11-23 16:10:10", "isend": 1, "rules": [{"id": 1, "mode": 1, "requirement": 100.0, "discount": 10.0}]}' in response.get_data(as_text=True))

#     def test_modifyPromotions(self):
#         response = self.client.post('http://localhost:5000/api/promotions/', data={
#             "theme": "端午节活动",
#             "begin": "2017-11-23 16:10:10",
#             "end": "2017-11-23 16:10:10",
#             "isend": 1
#         })
#         self.assertTrue('Login required.' in response.get_data(as_text=True))

#         response = self.client.post('http://localhost:5000/api/busers/session', data={
#             "username": "aaa",
#             "password": "123",
#         })
#         self.assertTrue("Successfully login." in response.get_data(as_text=True))

#         response = self.client.post('http://localhost:5000/api/promotions/', data={
#             "theme": "端午节活动",
#             "begin": "2017-11-23 16:10:10",
#             "end": "2017-11-23 16:10:10",
#             "isend": 1
#         })
#         self.assertTrue(response.status_code == 200)

#         response = self.client.put('http://localhost:5000/api/promotions/1', data={
#             "theme": "hhh",
#             "begin": "2017-01-01 16:10:10",
#             "end": "2017-01-02 16:10:10",
#             "isend": 2
#         })
#         self.assertTrue('modify promotion successfully' in response.get_data(as_text=True))

#     def test_deletePromotions(self):
#         response = self.client.post('http://localhost:5000/api/promotions/', data={
#             "theme": "端午节活动",
#             "begin": "2017-11-23 16:10:10",
#             "end": "2017-11-23 16:10:10",
#             "isend": 1
#         })
#         self.assertTrue('Login required.' in response.get_data(as_text=True))

#         response = self.client.post('http://localhost:5000/api/busers/session', data={
#             "username": "aaa",
#             "password": "123",
#         })
#         self.assertTrue("Successfully login." in response.get_data(as_text=True))

#         response = self.client.delete('http://localhost:5000/api/promotions/1')
#         # print(response.get_data(as_text=True))
#         self.assertTrue('delete promotion successfully.' in response.get_data(as_text=True))

#         response = self.client.get('http://localhost:5000/api/promotions/1')
#         # print(response.get_data(as_text=True))
#         self.assertTrue('promotion not found.' in response.get_data(as_text=True))
