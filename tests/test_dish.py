import unittest
from app import create_app, db

class FlaskClientTest(unittest.TestCase):

    dishes = [{"name": "毛血旺","category": "荤菜","price": 28.5,"stock": 99,"avaliable": 'True',"likes": 4,"description": "Hello 毛血旺"},
        {"name": "西红柿炒番茄","category": "素菜","price": 12.5,"stock": 99,"avaliable": 'True',"likes": 6,"description": "很难吃"},
        {"name": "马铃薯炒土豆","category": "素菜","price": 8.5,"stock": 99,"avaliable": 'True',"likes": 5,"description": "很好吃"},
        {"name": "红烧许琦","category": "荤菜","price": 128.5,"stock": 99,"avaliable": 'True',"likes": 100,"description": "哈哈"}]

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # response = self.client.post('http://localhost:5000/api/cuser/session', data={
        #     "username": "dfd",
        #     "role": "CUSTOMER"
        # })
        # self.assertTrue('Successfully login.' in response.get_data(as_text=True))

    def tearDown(self):
        # response = self.client.put('http://localhost:5000/api/cuser/session')
        # self.assertTrue('Successfully logout.' in response.get_data(as_text=True))

        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_addDish(self):
        for dish in self.dishes:
            response = self.client.post('http://localhost:5000/api/dish/', data=dish)
            self.assertTrue(200 == response.status_code)

    def test_getDish(self):

        for dish in self.dishes:
            response = self.client.post('http://localhost:5000/api/dish/', data=dish)
            self.assertTrue(200 == response.status_code)

        for id in range(1, 5):
            url = 'http://localhost:5000/api/dish/did/' + str(id)
            response = self.client.get(url)
            self.assertTrue(200 == response.status_code)
            if id == 1:
                print(dir(response))

    # def test_modifyDish(self):
    #     for dish in self.dishes:
    #         response = self.client.post('http://localhost:5000/api/dish/', data=dish)
    #         self.assertTrue(200 == response.status_code)

    #     new_dish = self.dishes[0]
    #     new_dish['likes'] = 0
    #     response = self.client.put('http://localhost:5000/api/dish/did/1', data=new_dish)
    #     self.assertTrue(200 == response.status_code)

    #     id = int(response.json['dishId'])
    #     url = 'http://localhost:5000/api/dish/did/' + str(id)
    #     response = self.client.get(url)
    #     self.assertTrue(200 == response.status_code)
    #     # self.assertTrue(0 == int(res.json['likes']))

    # def test_deleteDish(self):
    #     tmp_dish = self.dishes[0]
    #     tmp_dish['name'] = '清蒸提莫'
    #     response = self.client.post('http://localhost:5000/api/dish/', data=tmp_dish)
    #     self.assertTrue(200 == response.status_code)

    #     id = int(response.json['dishId'])

    #     url = 'http://localhost:5000/api/dish/did/' + str(id)
    #     response = self.client.delete(url)
    #     self.assertTrue(200 == response.status_code)

    # def test_getDishByCat(self):
    #     response = self.client.get('http://localhost:5000/api/dish/category/荤菜')
    #     self.assertTrue(200 == response.status_code)
    #     # print(response.json)

    