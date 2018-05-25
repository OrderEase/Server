## How to run

Test in python3.6.

Create your own `instance/config.py` at root directory.

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

