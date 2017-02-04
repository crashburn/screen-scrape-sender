# Initial setup
This is a python project that uses Flask, and Flask highly recommends using
virtual environments.  If you don't have virtualenv installed and you are using
Mac or Linux, run
```
sudo pip install virtualenv
```

# Each session setup
Each time you are going to work on the project first run virutalenv:
```
. venv/bin/activate
```
then set the flask environment variable
```
export FLASK_APP=hello.py
```
then finally run the flask application
```
flask run
```
At the time of this writing, all of this info is available in more detail on the
Flask website http://flask.pocoo.org/docs/0.12/quickstart/
