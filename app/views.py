from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from app.models import Links, Users
import re, urllib, urllib2, json


    ## URL Shortener related views ##


# Index - Homepage #


def index(request):
    result = {}

    # This will be used to hyper link the logo in the result page

    result['root_url'] = "http://" + request.get_host()

    # If the user is signed in then get the user details from the session and pass those to the 'index.html' template

    if 'username' in request.session:
        result['logged_in'] = 1
        result['username'] = request.session['username']
        result['first_name'] = request.session['first_name']
    else:

        # Otherwise just pass 0 to notify that the user is not logged in

        result['logged_in'] = 0
    return render(request, 'index.html', {'result' : result})


# REST API - GET the url back for a particular token #


def rest_get(request, token):
    result = {}

    # Regex to accept only valid token. Valid tokens contain a-z and 0-9

    pattern = re.compile("^[a-z0-9]+$")

    # Check the token with the pattern and fill the result dictionary accordingly

    if pattern.match(token):
        details = Links.get_url(Links, token)
        if len(details) > 0:
                result['status'] = 200
                result['status_message'] = "OK"
                result['url'] = urllib.unquote(details[0].url)
        else:
                result['status'] = 404
                result['status_message'] = "Not Found"
                result['url'] = None
    else:

        # Invalid token

        result['status'] = 400
        result['status_message'] = "Bad Request"
        result['url'] = None

    # Return the dictionary as a JSON response

    return JsonResponse(result)


# REST API - POST the url and get a new token back #


def rest_post(request, url):
    url = request.get_full_path()[11:]
    result = {}
    # Regex to accept only valid URLs

    pattern = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

    # Check the URL with the pattern and fill the result dictionary accordingly

    if pattern.match(url):
        url = urllib.quote(url)
        details = Links.get_token(Links, url)
        if len(details) > 0:
                result['status'] = 201
                result['status_message'] = "Created"
                result['token'] = details[0].token
        else:
                result['status'] = 404
                result['status_message'] = "Not Found"
                result['token'] = None

    # Invalid URL

    else:
        result['status'] = 400
        result['status_message'] = "Bad Request"
        result['token'] = None

    # Return the dictionary as a JSON response

    return JsonResponse(result)


# View a token #


def view(request, token):

    # Generate the target URL to call the API

    target_url = "http://" + request.get_host() + "/rest/get/" + token

    # Get the details and extract it out of the REST API response

    token_details = urllib2.urlopen(target_url).read()
    result = json.loads(token_details)

    # If the token is valid then unquote the URL and redirect to that

    if result['status']>=200 and result['status']<=299:
        return redirect(urllib.unquote(result['url']))

    # Otherwise display an error message

    else:
        result['error'] = 1
        result['root_url'] = "http://" + request.get_host()
        return render(request, 'result.html', {'result': result})


# Create a token for a URL #


def create(request):

    # If this is a valid request then only create a new token

    if 'url' in request.POST:

        # Generate the target URL to call the API

        target_url = "http://" + request.get_host() + "/rest/post/" + request.POST['url']

        # Get the details and extract it out of the REST API response

        details = urllib2.urlopen(target_url).read()
        result = json.loads(details)

        # Check the status of the request and fill the dictionary accordingly and display the data using 'result.html'

        if result['status']>=200 and result['status']<=299:
            result['error'] = 0
            result['data'] = "http://" + request.get_host() + "/view/" + result['token']
        else:
            result['error'] = 1
        return render(request, 'result.html', {'result': result})

    # If this isn't a valid request, redirect back to the homepage

    else:
        return redirect("http://" + request.get_host())



    ## User sign in / sign out / sign up related views ##



# Sign up #


def signup(request):

    # If the use user is already logged in redirect back to the homepage

    if 'username' in request.session:
        return redirect("http://" + request.get_host())

    # Otherwise process the sign up request

    result = {}
    result['root_url'] = "http://" + request.get_host()

    # Check if the mandatory fields of the form are set or not

    if 'username' in request.POST and 'email' in request.POST and 'password' in request.POST:

        # If the username, password and the email is in the valid format

        if check_username(request, request.POST['username']) and check_password(request, request.POST['password']) and check_email(request, request.POST['email']) and check_name(request, request.POST['first_name'], 1) and check_name(request, request.POST['last_name'], 1):
            details = {}
            details['username'] = request.POST['username']
            details['password'] = request.POST['password']
            details['email'] = request.POST['email']
            details['first_name'] = request.POST['first_name']
            details['last_name'] = request.POST['last_name']

            # Strict validation. Mode 2 is used. Check the method check_name(request, name, mode) for details.

            if not check_name(request, request.POST['first_name'], 2):
                details['first_name'] = details['username']
            result = Users.new_user(Users, details)
        else:
            result['status'] = 0
            result['status_message'] = 'Invalid input. Check the constraints.'
    else:
        result['status'] = 0
        result['status_message'] = 'Mandatory fields: Username, Email, Password'

    # If the signup is successful, set the session variables and redirect it back to the homepage

    if result['status']:
        request.session['username'] = details['username']
        request.session['first_name'] = details['first_name']
        return redirect("http://" + request.get_host())

    # Otherwise go back to the signup page with the error messages

    else:
        return render(request, 'signup.html', {'result' : result})


# Sign in #


def signin(request):

    # If the use user is already logged in redirect back to the homepage

    if 'username' in request.session:
        return redirect("http://" + request.get_host())
    result = {}
    result['root_url'] = "http://" + request.get_host()

    # Check if the mandatory fields of the form are set or not

    if 'username' in request.POST and 'password' in request.POST:

        # If the username is in the valid format

        if check_username(request, request.POST['username']):
            result = Users.validate(Users, request.POST['username'], request.POST['password'])
        else:
            result['status'] = 0
            result['status_message'] = 'Invalid username'
    else:
        result['status'] = 0
        result['status_message'] = 'Enter username and password'

    # If the login is successful fill the session variables and redirect back to the homepage

    if 'status' in result and result['status'] == 1:
        request.session['username'] = request.POST['username']
        request.session['first_name'] = result['first_name']
        return redirect("http://" + request.get_host())

    # Otherwise go back to the signin page with the error messages

    else:
        return render(request, 'signin.html', {'result' : result})


# Sign out #


def signout(request):

    # Clear the session variables and redirect back to the homepage

    del request.session['username']
    del request.session['first_name']
    return redirect("http://" + request.get_host())


# Method to check if the username format is valid or not #


def check_username(request, username):

    # Regex pattern to accept a-z, A-Z, 0-9 with two special characters: . and _

    pattern = re.compile("^[a-zA-Z0-9._]+$")
    if pattern.match(username) and len(username)<=32:
        return True
    else:
        return False


# Method to check if the password format is valid or not #


def check_password(request, password):
    if len(password) < 8 or len(password) > 64:
        return False
    else:
        return True


# Method to check if the email format is valid or not #


def check_email(request, email):

    # Regex pattern to check if the email is valid or not

    pattern = re.compile("[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+")
    if pattern.match(email):
        return True
    else:
        return False


# Method to check if the name format is valid or not #


def check_name(request, name, mode):

    # Mode 1 is the basic validation. Its not mandatory for the name to be present. The name can be an empty string also.

    if mode==1:
        pattern = re.compile("^[a-zA-Z]*$")

    # Mode 2 is the strict validation. It only passes strings containing only a-z and A-Z.

    elif mode==2:
        pattern = re.compile("^[a-zA-Z]+$")

    # Match the name with the required regex generated above.

    if pattern.match(name) and len(name) <= 64:
        return True
    else:
        return False