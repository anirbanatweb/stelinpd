from django.db import models
import hashlib, uuid


    ## Class - Links and related methods ##


class Links(models.Model):

    # Table structure

    id = models.AutoField(primary_key=True)
    url = models.TextField()
    token = models.CharField(max_length=128)

    def __unicode__(self):
        return u"%s %s %s" % (self.id, self.url, self.token)


    # GET URL for a token #


    @staticmethod
    def get_url(self, token):
        result = Links.objects.filter(token=token)
        return result


    # GET TOKEN for a URL #


    @staticmethod
    def get_token(self, url):

        # Check if the URL already exists or not

        result = Links.if_url_exists(self, url)

        # If the URL doesn't exist calculate a token and store that in the database

        if len(result) == 0:
            query = Links(url=url)
            query.save()
            obj = Links.objects.filter(url=url)[0]
            token = Links.base_convert(obj.id+1000000, 36)
            obj.token = token
            obj.save()
            result = Links.objects.filter(id=obj.id)
        return result


    # Helper method for get_token(self, url). It checks if the database already contains the URL #


    @staticmethod
    def if_url_exists(self, url):
        result = Links.objects.filter(url=url)
        return result


    # Helper method to calculate the token. It converts the id of base 10 to base 36 #


    @staticmethod
    def base_convert(n, base):
        digits = "0123456789abcdefghijklmnopqrstuvwxyz"
        try:
            n = int(n)
            base = int(base)
        except:
            return ""
        if n < 0 or base < 2 or base > 36:
            return ""
        s = ""
        while 1:
            r = n % base
            s = digits[r] + s
            n /= base
            if n == 0:
                break
        return s



    ## Class Users and related methods ##



class Users(models.Model):

    # Table structure

    username = models.SlugField(max_length=32, primary_key=True)
    email = models.EmailField()
    password_hash_salt = models.TextField()
    password = models.TextField()
    first_name = models.TextField(max_length=64, blank=True)
    last_name = models.TextField(max_length=64, blank=True)

    def __unicode__(self):
        return u"%s %s %s %s" % (self.username, self.email, self.first_name, self.last_name)


    # Create a new user #


    @staticmethod
    def new_user(self, new_user_details):
        result = {}

        # Check if the username exists or not.

        if Users.check_if_username_exists(self, new_user_details['username']):
            result['status'] = 0
            result['status_message'] = 'Username already exists'

        # Check if the email exists or not.

        elif Users.check_if_email_exists(self, new_user_details['email']):
            result['status'] = 0
            result['status_message'] = 'Email already exists'

        # If username and email doesn't exist then sign the user up

        else:

            # Generate a password hash salt

            password_hash_salt = uuid.uuid4().hex

            # Generate a hashed password using the salt and the password. Store both the salt and the hashed password.

            hashed_password = Users.calculate_hashed_password(self, new_user_details['password'], password_hash_salt)
            query = Users(new_user_details['username'], new_user_details['email'], password_hash_salt, hashed_password, new_user_details['first_name'], new_user_details['last_name'])
            query.save()
            result['status'] = 1
            result['status_message'] = 'Successfully signed up'
        return result


    # Method to check if the username already exists or not #


    @staticmethod
    def check_if_username_exists(self, username):
        details = Users.objects.filter(username = username)
        if len(details) > 0:
            return True
        else:
            return False


    # Method to check if the email already exists or not #


    @staticmethod
    def check_if_email_exists(self, email):
        details = Users.objects.filter(email = email)
        if len(details)>0:
            return True
        else:
            return False


    # Calculate the hashed password using the password and a salt #


    @staticmethod
    def calculate_hashed_password(self, password, password_hash_salt):
        hashed_password = hashlib.sha512(password + password_hash_salt).hexdigest()
        return hashed_password


    # Validate the username/password combinations #


    @staticmethod
    def validate(self, username, password):
        result = {}

        # If the username exists or not

        if Users.check_if_username_exists(self, username):

            # Get the salt used during sign up. Use that salt to generate the hashed password and match it #

            details = Users.objects.filter(username = username)
            password_hash_salt = details[0].password_hash_salt
            hashed_password = Users.calculate_hashed_password(self, password, password_hash_salt)

            # If the newly calculated hashed password is same as the stored password

            if hashed_password == details[0].password:
                result['status'] = 1
                result['status_message'] = 'Successfully validated'
                result['first_name'] = details[0].first_name

            # If those are not the same

            else:
                result['status'] = 0
                result['status_message'] = 'Validation failed'

                # If the username doesn't exist

        else:
            result['status'] = 0
            result['status_message'] = 'Username doesn\'t exist'
        return result