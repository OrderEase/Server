# from app import create_app, db
from requests import Session, post, put, get

def main():
    s = Session()
    # login a business user
    response =s.post('http://localhost:5000/api/buser/', data={
        "restId": 1,
        "username": "aaa",
        "role": "BUSINESS",
        "password": "123",
        "authority": "MANAGER"})
    if (response.status_code == 500):
        pass

    response = s.post('http://localhost:5000/api/buser/session', data={
        "username": "aaa",
        "restId": 1,
        "password": "123",
        "role": "BUSINESS"
    })
    if (response.status_code != 200):
        print("Login business user failed!")
        return 

    buid = response.json()['buser_id']

    # modify a restaurant
    url = 'http://localhost:5000/api/rstr/buid/' + str(buid)
    response = s.put(url, data={
            'name':'点都德',
            'info': '茶楼'
            })
    if (response.status_code != 200):
        print("Modify Rstr failed!")
        return 

    # add some dishes
    dishes = [{"name": "毛血旺","category": "荤菜","price": 28.5,"stock": 99,"avaliable": 'True',"likes": 4,"description": "Hello 毛血旺"},
        {"name": "西红柿炒番茄","category": "素菜","price": 12.5,"stock": 99,"avaliable": 'True',"likes": 6,"description": "很难吃"},
        {"name": "马铃薯炒土豆","category": "素菜","price": 8.5,"stock": 99,"avaliable": 'True',"likes": 5,"description": "很好吃"},
        {"name": "红烧许琦","category": "荤菜","price": 128.5,"stock": 99,"avaliable": 'True',"likes": 100,"description": "哈哈"}]
    dishId = []
    for dish in dishes:
        response = s.post('http://localhost:5000/api/dish/', data=dish)
        if (response.status_code == 200):
            dishId.append(response.json()['dishId'])
        elif (response.json()['message'] == 'Dish name already exist'):
            dishId.append(response.json()['dishId'])
        else:
            print("Add dishes failed!")
            return

    # add a menu
    dishesStr = ''
    for i in range(len(dishId)):
        dishesStr += str(dishId[i])
        if i != len(dishId)-1:
            dishesStr += ','

    response = s.post('http://localhost:5000/api/rstr/buid/1/menu',
                                data={
                                'name':'春季菜单',
                                'dishes':dishesStr
                                })
    if (response.status_code != 200 and response.json()['message'] != 'Name already exists.'):
        print("Add menu failed!")
        return 

if __name__ == '__main__':
    main()