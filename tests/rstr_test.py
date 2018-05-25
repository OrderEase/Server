from requests import put, get, post, delete
import json

class TestRstr():
    def addRstr(self):
        res = post('http://localhost:5000/api/rstr/', data={'name':'点都德', 'info': '茶楼'})
        if res.status_code != 200:
            print(res.json()['message'])
            return

    def postMenu(self):
        res = post('http://localhost:5000/api/rstr/1', data={'name':'春季菜单', 'dishes':'1,2,3,4'})
        if res.status_code != 200:
            print(res.json()['message'])
            return

    def getRstr(self):
        res = get('http://localhost:5000/api/rstr/1')
        if res.status_code != 200:
            print(res.json()['message'])
            return
        print(res.json())
