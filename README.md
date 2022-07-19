# Image-clasiffier

## Database requirements

you should already have a working database running on a server

## Installation

This is a flask web application so if the installation is in a brand new instance you need to install python and a SQL database
check [Python](https://www.python.org/downloads/)

The next step is to install the lib to create virtual environments in python

```bash
sudo apt-get install python3-venv
```

once you get a correct install, clone this repository

when you have successfully cloned the repository create a virtual environment with this command

```bash
python3 -m venv virtual-environment-name
```

you can activate your virtual environment

Linus

```bash
source venv/bin/activate
```

you will see this prompt in your console

```bash
(virtual-environment-name) $
```

now install all the dependecies of the app with

```bash
pip install -r requirements.txt
```

with the dependecies installed now we have 2 options we can run a dev server or run the app on the production server

### Dev server

You have to set to enviroment variables that flask needs to run the server:

```bash
export FLASK_APP=classifier.py
```

```bash
export FLASK_DEBUG=1
```

```bash
export DEV_DATABASE_URL=mysql+pymysql:<sql_connection_string>
```

then run the server:

```bash
flask run
```

it will serve the app in localhost:5000

### Production

you can set the database env if you are going to launch the app immediately

```bash
export DATABASE_URL=mysql+pymysql:<sql_connection_string>
```

launch the app

```bash
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

if we create a sertvice we need to create a .env file with the DATABASE_URL=mysql+pymysql:<sql_connection_string> value

then we need create a service with

```bash
sudo nano /etc/systemd/system/myproject.service
```

the user of linus shuld be in Group=www-data
the content of the file should be

```bash
[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=<user>
Group=www-data
WorkingDirectory=/home/<user>/<myproject>
Environment="PATH=/home/<user>/<myproject>/myprojectenv/bin"
ExecStart=/home/<user>/<myproject>/myprojectenv/bin/gunicorn --bind 0.0.0.0:5000 wsgi:app

[Install]
WantedBy=multi-user.target
```

the wsgi.py it's the app factory you can change what config to use to create your apps (configs are in config.py)

wsgi.py

```python
from app import create_app

app =  create_app(<config to use>)

if __name__ == "__main__":
    app.run()
```

## Pre Installed commands

when you are in your virtual environment with all the dependencies installed and the FLASK_APP environment variable set flask makes available some customized commands

deploy runs all the migrations when you have a brand new databese

```bash
flask deploy
```

sroles seeds defaults roles for the user should be used before creating any user

```bash
flask sroles
```

addfirsttestuser add a test user with email test_user@test.com and a default password

```bash
flask addfirsttestuser
```

adduser add a user from pased args email, name, lastName, password separeted by spaces

```bash
flask adduser myname@gmail.com Pedro Gonzales SuPerPass!*
```
