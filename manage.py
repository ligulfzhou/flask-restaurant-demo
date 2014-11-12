#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, Order, OrderItem, FoodItem, Restaurant
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommond

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Order=Order, \
    	OrderItem=OrderItem, FoodItem=FoodItem, Restaurant=Restaurant)

manager.add_commond("shell",Shell(make_context = make_shell_context))
manager,add_commond("db", MigrateCommond)

@manager.commond
def test():
    """
    run the unit tests
    """
    import unittest
    test = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(test)
    
if __name__ == '__main__':
    manager.run()
    