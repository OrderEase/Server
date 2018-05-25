from requests import put, get, post, delete
import json

myorder1 = {"tableId": "23E","dishes": "1, 2"}
myorder1 = {"tableId": "23E","dishes": "3, 2"}

class TestOrder():
    orderId = 1
    cuid = 1
    def postOrder(self):
        res = post('http://localhost:5000/api/order/cuid/1', data=myorder1)
        if res.status_code != 200:
            print(res.json()['message'])
            return
        self.orderId = int(res.json()['orderId'])

    def getOrder(self):
        res = get('http://localhost:5000/api/order/cuid/1/oid/1')
        if res.status_code != 200:
            print(res.json()['message'])
            return
        print(res.json())

    def payOrder(self):
        res = put('http://localhost:5000/api/order/cuid/1/oid/1', data={'payId': 100})
        if res.status_code != 200:
            print(res.json()['message'])
            return
        res = get('http://localhost:5000/api/order/cuid/1/oid/1')
        if res.status_code != 200:
            print(res.json()['message'])
            return
        print(res.json())

