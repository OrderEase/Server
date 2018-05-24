from requests import put, get, post
import json

res = post('http://localhost:5000/api/dish/', data={
  "name": "毛血旺",
  "category": "荤菜",
  "price": 28.5,
  "stock": 99,
  "avaliable": 'True',
  "likes": 4,
  "description": "Hello 毛血旺"
}).json()

print(res)
