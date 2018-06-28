# import unittest
# import json
# from app import create_app, db

# class FlaskClientTest(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app()
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#         self.client = self.app.test_client()

#     def tearDown(self):
#         self.app_context.pop()

#     # def test_register(self):
#     #     response = self.client.post('http://localhost:5000/api/busers/', data=json.dumps({
#     #         "username": "aaabbb",
#     #         "password": "1232",
#     #         "authority": "manager"}))
#     #     # print(response.get_data(as_text=True))
#     #     self.assertTrue(response.status_code == 200)

#     def test_login(self):
#         response = self.client.post('http://localhost:5000/api/busers/session', data=json.dumps({
#             "username": "manager",
#             "password": "123"
#         }))
#         # print(response.get_data(as_text=True))
#         self.assertTrue("Successfully login." in response.get_data(as_text=True))

#         response = self.client.post('http://localhost:5000/api/busers/session', data=json.dumps({
#             "username": "aada",
#             "password": "123"
#         }))
#         print(response.get_data(as_text=True))
#         self.assertTrue("Invalid username or password." in response.get_data(as_text=True))

#         response = self.client.post('http://localhost:5000/api/busers/session', data=json.dumps({
#             "username": "aaa",
#             "password": "1dd23"
#         }))
#         # print(response.json)
#         self.assertTrue("Invalid username or password." in response.get_data(as_text=True))

#     def test_logout(self):
#         response = self.client.put('http://localhost:5000/api/busers/session')

#         response = self.client.post('http://localhost:5000/api/busers/session', data=json.dumps({
#             "username": "aaa",
#             "password": "123",
#         }))
#         # print(response.get_data(as_text=True))
#         self.assertTrue("Successfully login." in response.get_data(as_text=True))

#         response = self.client.put('http://localhost:5000/api/busers/session')
#         # print(response.get_data(as_text=True))
#         self.assertTrue('Successfully logout.' in response.get_data(as_text=True))

#     def test_modifyPassword(self):
#         response = self.client.put('http://localhost:5000/api/busers/password', data=json.dumps({
#             "username": "aaa",
#              "oldPassword": "123",
#             "newPassword": "111"
#         }))
#         # print(response.get_data(as_text=True))
#         self.assertTrue('Login required.' in response.get_data(as_text=True))

#         response = self.client.post('http://localhost:5000/api/busers/session', data=json.dumps({
#             "username": "aaa",
#             "password": "123"
#         }))
#         self.assertTrue("Successfully login." in response.get_data(as_text=True))

#         response = self.client.put('http://localhost:5000/api/busers/password', data=json.dumps({
#             "username": "aaa",
#             "oldPassword": "123",
#             "newPassword": "111"
#         }))
#         # print(response.get_data(as_text=True))
#         self.assertTrue("Change password successfully." in response.get_data(as_text=True))

#         response = self.client.post('http://localhost:5000/api/busers/session', data=json.dumps({
#             "username": "aaa",
#             "password": "123"
#         }))
#         self.assertTrue("Invalid username or password." in response.get_data(as_text=True))

#         response = self.client.post('http://localhost:5000/api/busers/session', data=json.dumps({
#             "username": "aaa",
#             "password": "111"
#         }))
#         self.assertTrue("Successfully login." in response.get_data(as_text=True))

#     # def test_avatar(self):
#     #     response = self.client.post('http://localhost:5000/api/busers/session', data=json.dumps({
#     #         "username": "aaa",
#     #         "password": "123"
#     #     }))
#     #     self.assertTrue("Successfully login." in response.get_data(as_text=True))

#         # response = self.client.get('http://localhost:5000/api/busers/avatar')
#         # # print(response.get_data(as_text=True))
#         # self.assertTrue("default.png" in response.get_data(as_text=True))

#         # response = self.client.put('http://localhost:5000/api/busers/avatar', data=json.dumps({
#         #     "data": "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
#         # }))
#         # self.assertTrue("Successfully modify avatar." in response.get_data(as_text=True))

#         # response = self.client.get('http://localhost:5000/api/busers/avatar')
#         # # print(response.get_data(as_text=True))
#         # self.assertTrue("4a47a0db6e60853dedfcfdf08a5ca249.png" in response.get_data(as_text=True))

