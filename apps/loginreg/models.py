from __future__ import unicode_literals

from django.db import models

import re

from django.contrib import messages

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
FIRSTNAME_REGEX = re.compile(r'^[a-zA-Z]')
LASTNAME_REGEX = re.compile(r'^[a-zA-Z]')

# Create your models here.

class UserManager(models.Manager):
    def register(self, email,  first_name, last_name, password, passwordconfirmation):
        errorsforreg = []
        no_same_email = True
        if len(email) < 1 and not EMAIL_REGEX.match(email):
            errorsforreg.append("Email must not be empty or must be in good format -> asdf@mail.com!")
        
        try:
            checkforsameemail = User.userManager.get(email=email)
            errorsforreg.append("Opps! Looks like this email already exists in our database!")
            no_same_email = False
        except:
            no_same_email = True

        if len(first_name) < 2 and not FIRSTNAME_REGEX.match(first_name):
            errorsforreg.append("Firstname must not be empty or must only have letters!")
        if len(last_name) < 2 and not LASTNAME_REGEX.match(last_name):
            errorsforreg.append("Last Name must not be empty or must only have letters!")
        if len(password) < 8 and len(passwordconfirmation) < 1:
            errorsforreg.append("Password and password confirmation must not be empty!")
        if password != passwordconfirmation:
            errorsforreg.append("Password and password confirmation must match!")

        if not errorsforreg:
            user = User.userManager.create(first_name = first_name, last_name = last_name, email = email, password = password)
            return {"status": True, "sameemail": no_same_email, "data": user}
        else:
            return {"status": False, "sameemail": no_same_email, "data": errorsforreg}

    def login(self, emailforlogin, passwordforlogin):
        errors = []

        if len(emailforlogin) < 1:
            errors.append("Email must not be empty or must have more than 2 characters")
        if not EMAIL_REGEX.match(email): # email regex
            errors.append("Email must not be empty or must be in good format -> asdf@mail.com!")
        
        
        if len(passwordforlogin) < 1:
            errors.append("Password must not be empty or must have more than 2 characters!")

        if not errors:
            user_list = User.userManager.filter(email = emailforlogin)
            if user_list:
                getuser = user_list[0]
                if getuser.password == passwordforlogin:
                    user = User.userManager.get(email = emailforlogin, password = passwordforlogin)
                    return {"status": True, "data": user}
                else:
                    errors.append("Password is wrong!")
            else:
                errors.append("Opps! Not in our database! Register! Please!")

        return {"status": False, "data": errors}     


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    userManager = UserManager()
