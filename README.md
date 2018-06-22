# OrderEase Server
[![Build Status](https://travis-ci.org/OrderEase/Server.svg?branch=master)](https://travis-ci.org/OrderEase/Server)
[![Coverage Status](https://coveralls.io/repos/github/YHJRUBY/OrderEase-Server/badge.svg?branch=master)](https://coveralls.io/github/YHJRUBY/OrderEase-Server?branch=master)
[![GPL Licence](https://badges.frapsoft.com/os/gpl/gpl.svg?v=103)](https://opensource.org/licenses/GPL-3.0/)


## How to run

Test in python3.6.

To connect to your own DB, you should create your own `instance/config.py` at root directory, such as:

```python
SQLALCHEMY_DATABASE_URI="mysql://username:password@localhost:3306/test?charset=utf8"
SQLALCHEMY_TRACK_MODIFICATIONS=True
SECRET_KEY = 'Sdna2MshdG39DOA2skajd'
```

Create the virtual environmet:

```shell
python -m venv venv
```

Activate the virtual environment:

```shell
. venv/bin/activate
```

Install dependencies:

```shell
pip install -r requirements.txt
```

Start the server:

```shell
python manage.py runserver
```

Run all the unit tests:

```python
python manage.py test
```

## How to add some dishes and menu when testing 2C without minding 2B
run `temp/add.py`


After that, four dishes would be added into the database, and a menu would be created and associated with the restaurant.
