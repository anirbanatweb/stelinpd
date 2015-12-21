# Stelinpd
**Shorten URLs quickly!**

Stelinpd is a basic URL shortener developed using HTML, CSS, Python, Django and a bit of JavaScript. These are the basic features of the application:

* Shorten URLs and view them later.
* Implemented using REST APIs, so it will be easy to create an app for other mobile platforms later if required.
* It also has options for the user to sign up / sign in.

## Stack used

Python - Django - WSGI

* Python 2.7.11
* Django 1.8

Also SQLite is used during the development / testing. But you are free to use any supported database of your choice. You just need to change the `DATABASES` settings in `stelinpd/settings.py`.

## Database Structure

Two tables are used in this application. Structures of those are given below:

* `Links (id, url, token)`

  * `id` : AutoField  (`Primary key`)
  * `url` : TextField
  * `token` : CharField

* `Users (username, email, password_hash_salt, password, first_name, last_name)`

  * `username` : SlugField (`Primary key`)
  * `email` : EmailField
  * `password_hash_salt` : TextField
  * `password` : TextField
  * `first_name` : TextField
  * `last_name` : TextField


## Installation

Installation of the web app is easy! Just follow the given steps:

* Make sure you have Python 2.7 and Django 1.8 installed.
* Download this zip file.
* Extract it anywhere.
* Open the command prompt / console and go to the directory where you have extracted the files.
* Type these commands:
  * `python manage.py makemigrations app`
  * `python manage.py migrate`
  * `python manage.py runserver`
* `Disable ad blockers`. Otherwise the `Sign out` button may not appear.

And that is all!

In case you are facing any error. Try these:
* Type `python manage.py check` to check if there are any issues. Ideally this should return `System check identified no issues (0 silenced)`.
* Type `python manage.py syncdb`.

## How to start

### Application

Enter the address displayed on your command prompt / console. For example if you are seeing this,
```
System check identified no issues (0 silenced).
December 21, 2015 - 02:44:06
Django version 1.8, using settings 'stelinpd.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Then open the address `http://127.0.0.1:8000/` using your favorite browser (preferably Google Chrome).

### REST API

Stelinpd offers two APIs, one to get the token for a particular URL and the other one to get the URL back for a particular token. Data will be returned in the `JSON` format. Let's see these in detail:

##### Get the token for a particular URL

You need to call the `<address of the root>/rest/post/<URL>`. For example, if your URL is `https://www.wikipedia.org/` then you should call,

`http://127.0.0.1:8000/rest/post/https://www.wikipedia.org/`

##### Get the URL back for a particular token

You need to call the `<address of the root>/rest/get/<token>`. For example, if your token is `lfly` then you should call,

`http://127.0.0.1:8000/rest/get/lfly/`
