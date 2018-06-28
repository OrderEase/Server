# OrderEase Server
![Progress](http://progressed.io/bar/50?title=completed)
[![Build Status](https://travis-ci.org/OrderEase/Server.svg?branch=master)](https://travis-ci.org/OrderEase/Server)
[![Coverage Status](https://coveralls.io/repos/github/OrderEase/Server/badge.svg?branch=master)](https://coveralls.io/github/OrderEase/Server?branch=master)
[![GPL Licence](https://badges.frapsoft.com/os/gpl/gpl.svg?v=103)](https://opensource.org/licenses/GPL-3.0/)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

## How to run

Test in python3.6.

To connect to your own DB, you should create your own `instance/config.py` at root directory, such as:

```python
SQLALCHEMY_DATABASE_URI="mysql://username:password@localhost:3306/test?charset=utf8"
SQLALCHEMY_TRACK_MODIFICATIONS=True
SECRET_KEY = 'Sdna2MshdG39DOA2skajd'
GEN_FAKE_DATA = True
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

You should create basic data first:

```python
python manage.py gen_data
```

Start the server:

```shell
python manage.py runserver
```

Run all the unit tests: (not finished)

```python
python manage.py test
```
