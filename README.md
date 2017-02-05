# Initial setup
This is a python project, so make sure you have python installed.  Python
should be pre-installed if you are using a Mac or Linux.  Windows does not
have it by default.  Open a command window and type `python --version` to
confirm.  This project is confirmed to work with version 2.7.12.

If you don't already have it, install the pip package manager.  The way to
do this varies based on the platform.  On Linux Mint I used
```
sudo apt-get install python-pip
```
Other platorms are listed here
https://packaging.python.org/install_requirements_linux/#installing-pip-setuptools-wheel-with-linux-package-managers

This is project uses Flask, and Flask highly recommends using
virtual environments.  If you don't have virtualenv installed and you are using
Mac or Linux, run
```
sudo pip install virtualenv
```
Next, activate the virtual environment
```
. venv/bin/activate
```
Finally, install Flask and gevent
```
pip install flask gevent
```

# Each session setup
Each time you are going to work on the project first run virutalenv:
```
. venv/bin/activate
```
then finally run the application
```
python event-engine.py
```

# Bookmarklet
Bookmarklets are little snippets of javascript code that you can save as a
bookmark in you browser.  When you click the bookmark, the javascript runs
against the currently open page.

The included bookmarklet reads movie titles and ratings from the IMDb site,
and then sends that data to our "event engine" application.  It does this by
querying the DOM to find the data values and then putting the values into a
JSON object.  Then it creates a new img tag with a src attribute pointing to
the `publish` endpoint of event engine application.  Data is passed in the
query string.

To install the bookmarklet in Chrome:
  1. right-click on the bookmark bar in Chrome (you may need to enable the
  bookmark bar in settings)
  1. Choose `add page`
  1. Give the bookmarklet any name you want, such as `IMDb scraper`
  1. Paste the entire contents of `imdb_bookmarklet` into the "URL" field of
  the bookmark
  1. Save the bookmark

# Sending events
Once you have the bookmarklet installed and the event engine running, open
one browser window to http://127.0.0.1:5000/ and a second window to your
favorite movie listing in IMDb.  Click the bookmarklet while on the IMDb
page.  Check the other window for the movie title and content rating.
