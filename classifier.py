from email.utils import formatdate
import os
import re
from app import create_app, db
import datetime
import math
import click
from decimal import Decimal, localcontext, ROUND_05UP
from app.models import RateUser, Role
from flask_migrate import Migrate, upgrade

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db, render_as_batch=True)


@app.shell_context_processor
def make_shell_context():
    #assumptions
    return dict(db=db, User = RateUser)

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()


@app.cli.command('create_db')
def createDatabase():
    """Create the db based on the model difined"""
    db.create_all()
    print('***** Datebase created ****')

@app.cli.command()
def addFirstTestUser():
    """add a test user"""
    try:
        RateUser.add_test_user()
        db.session.commit()
        print("email:test_user@test.com password:test1234")
    except Exception as e:
        print(e)
        print("Error seeding user into the database")

@app.cli.command()
@click.argument('email')
@click.argument('name')
@click.argument('lastname')
@click.argument('password')
def addUser(email,name, lastname, password):
    """add a user from args email, name, lastName, password all separated by spaces in that order"""

    if re.search("[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", email):
        try:
            RateUser.add_user(email, name, lastname, password)
            db.session.commit()
            print(" User {} {} created with email: {}".format(name, lastname, email))
        except  Exception as e:
            print("Error seeding user into the database")
            print(e)
    else:
        print("{} its not a valid email")

@app.cli.command()
def sroles():
    """Run seeder tasks for roles"""
    # migrate database to latest revision
    Role.insert_roles()
    db.session.commit()

@app.template_filter()
def numberFormat(value):
    return "{0:,.2f}".format(value)

@app.template_filter()
def numberFormatInt(value):
    with localcontext() as ctx:
        ctx.rounding = ROUND_05UP
        deciaml_v =Decimal(value)
    return format(deciaml_v.to_integral_value(), ',f')

@app.template_filter()
def dateFormat(year,month, day):
    if day < 10 and day > 0:
        formattedDay = "0{}".format(day)
    elif day > 9 and day < 32:
        formattedDay = str(day)
    else:
        raise "Not a valid day  =  {}".format(day)

    if month < 10 and month > 0:
        formattedMonth = "0{}".format(month)
    elif month > 9 and month < 13:
        formattedMonth = str(month)
    else:
        raise "Not a valid month  =  {}".format(month)

    return "{}-{}-{}".format(year, formattedMonth,formattedDay)

