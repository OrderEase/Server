from requests import put, get, post
import app
import json
from app.models import User

db = app.db
app = app.create_app()


def test_dish():
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


def test_buser():
	buser = models.User(id='12345678999', password='123')
	db.session.add(buser)
	db.session.commit()

	result = models.User.query.get('12345678999')
	print(result)


def test_cuser():
	# cuser = User(username='12345678999', password='123', role='CUSTOMER')
	# db.session.add(cuser)
	# db.session.commit()
	client = app.test_client
	with client() as c:
		res = c.post('http://localhost:5000/api/cuser/session', data={
			"username": "12345678999",
 			"role": "CUSTOMER"
		}).json
		print(res)

		res = c.post('http://localhost:5000/api/cuser/session', data={
			"username": "dfdf",
 			"role": "CUSTOMER"
		}).json
		print(res)

		res = c.put('http://localhost:5000/api/cuser/session').json
		print(res)

test_cuser()


db.drop_all()
