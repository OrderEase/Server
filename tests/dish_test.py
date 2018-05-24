from requests import put, get, post, delete
import json

dishes = [{"name": "毛血旺","category": "荤菜","price": 28.5,"stock": 99,"avaliable": 'True',"likes": 4,"description": "Hello 毛血旺"},
{"name": "西红柿炒番茄","category": "素菜","price": 12.5,"stock": 99,"avaliable": 'True',"likes": 6,"description": "很难吃"},
{"name": "马铃薯炒土豆","category": "素菜","price": 8.5,"stock": 99,"avaliable": 'True',"likes": 5,"description": "很好吃"},
{"name": "红烧许琦","category": "荤菜","price": 128.5,"stock": 99,"avaliable": 'True',"likes": 100,"description": "哈哈"}]

class TestDish():
    def addDish(self):
        for dish in dishes:
            res = post('http://localhost:5000/api/dish/', data=dish)
            if res.status_code == 400 and res.json()['message'] == 'Dish name already exist':
                continue
            elif res.status_code == 200:
                continue
            else:
                print(res.json()['message'])
                return

    def getDish(self):
        for id in range(1, 5):
            url = 'http://localhost:5000/api/dish/did/' + str(id)
            res = get(url)
            if res.status_code != 200:
                print(res.json()['message'])
                return
            if i == 1:
                print(res.json())
    
    def modifyDish(self):
        new_dish = dishes[0]
        new_dish['likes'] = 0
        res = put('http://localhost:5000/api/dish/did/1', data=new_dish)
        if res.status_code != 200:
            print(res.json()['message'])
            return

        id = int(res.json()['dishId'])
        url = 'http://localhost:5000/api/dish/did/' + str(id)
        res = get(url, data=new_dish)
        if res.status_code != 200:
            print(res.json()['message'])
            return
        if int(res.json()['likes']) != 0:
            return

    def deleteDish(self):
        tmp_dish = dishes[0]
        tmp_dish['name'] = '清蒸提莫'
        res = post('http://localhost:5000/api/dish/', data=tmp_dish)
        id = -1
        if res.status_code == 400 and res.json()['message'] == 'Dish name already exist':
            pass
        elif res.status_code == 200:
            id = int(res.json()['dishId'])
        else:
            print(res.json()['message'])
            return

        url = 'http://localhost:5000/api/dish/did/' + str(id)
        res = delete(url)
        if res.status_code != 200:
            print(res.json()['message'])

    def getDishByCat(self):
        res = get('http://localhost:5000/api/dish/category/荤菜')
        print(res.json())