#!/usr/bin/env python
import os
from app import create_app, db
from flask_script import Manager, Shell, Server
import app.gen_data as data_generator

app = create_app('Development')
manager = Manager(app)

@manager.command
def test(coverage=False):
    """Run the unit tests."""
    data_generator.gen_basic_data()

    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def gen_data(coverage=False):
    """Generate fake data."""
    data_generator.gen_basic_data()

    if app.config['GEN_FAKE_DATA']:
        data_generator.gen_fake_data()
        data_generator.gen_unfinished_orders()

@manager.command
def del_data(coverage=False):
    """Generate fake data."""
    data_generator.remove_data()

@manager.command
def runserver(coverage=False):
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    manager.run()

# 设置 travis 集成