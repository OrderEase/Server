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
python manager.py runserver
```

Run all the unit tests:

```python
python manager.py test
```

