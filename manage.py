#!/usr/bin/env python
import os
from app import create_app, db
from flask_script import Manager, Shell

app = create_app()
manager = Manager(app)

import coverage
COV = coverage.coverage(branch=True, include='app/*')
COV.start()

@manager.command
def test(coverage=False):
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if coverage:

        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()



    # import unittest
    # tests = unittest.TestLoader().discover('tests')
    # unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
   manager.run()
