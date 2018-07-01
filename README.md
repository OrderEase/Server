# OrderEase Server
![Progress](http://progressed.io/bar/90?title=done)
[![Build Status](https://travis-ci.org/OrderEase/Server.svg?branch=master)](https://travis-ci.org/OrderEase/Server)
[![Coverage Status](https://coveralls.io/repos/github/OrderEase/Server/badge.svg?branch=master)](https://coveralls.io/github/OrderEase/Server?branch=master)
[![GPL Licence](https://badges.frapsoft.com/os/gpl/gpl.svg?v=103)](https://opensource.org/licenses/GPL-3.0/)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

## How to run

Test in python3.6.

**You should first set the following environment variable that you need. For instance, **

```python
MODE='DEVELOPMENT' # 'DEVELOPMENT', 'TEST' or 'PRODUCTION', default 'DEVELOPMENT'
PRODUCTION_DATABASE_URI="mysql://username:password@localhost:3306/prod?charset=utf8"
DEVELOPMENT_DATABASE_URI="mysql://username:password@localhost:3306/dev?charset=utf8"
TEST_DATABASE_URI="mysql://username:password@localhost:3306/test?charset=utf8"
SECRET_KEY = 'Sdna2MshdG39DOA2skajd'
```

The default config is in  `/app/config.py`.

Install dependencies:

```shell
pip install -r requirements.txt
```

Create basic data:

```python
python manage.py gen_basic_data
```

Create fake data for testing and presentation:

```python
python manage.py gen_fake_data
```

Start the server at `0.0.0.0:5000`:

```shell
python manage.py runserver
```

Run all the unit tests in TEST mode.

```python
python manage.py test
```
