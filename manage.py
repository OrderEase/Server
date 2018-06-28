#!/usr/bin/env python
import os
from app import create_app, db
from flask_script import Manager, Shell
import app.gen_data as data_generator

app = create_app()
manager = Manager(app)

@manager.command
def test(coverage=False):
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def gen_data(coverage=False):
    """Generate fake data."""
    data_generator.gen_basic_data()

    if app.config['GEN_FAKE_DATA']:
        data_generator.gen_fake_data()

@manager.command
def del_data(coverage=False):
    """Generate fake data."""
    data_generator.remove_data()

if __name__ == '__main__':
    manager.run()
