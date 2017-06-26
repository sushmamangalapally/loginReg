from django.shortcuts import render, redirect

# Create your views here.

import re

from django.contrib import messages

from .models import User

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
FIRSTNAME_REGEX = re.compile(r'^[a-zA-Z]')
LASTNAME_REGEX = re.compile(r'^[a-zA-Z]')


def index(request):
    return render(request, 'loginreg/index.html')

def login(request):
    if request.method == "POST":
        validations_for_login = User.userManager.login(request.POST['emailforlogin'], request.POST['passwordforlogin'])
        if validations_for_login['status']:
            request.session["userId"] = validations_for_login['data'].id
            return redirect('/success')
        else:
            messages.error(request, "Invalid email or password")
    return redirect('/')


def toregister(request):
    values_of_validations = User.userManager.register(request.POST['email'], request.POST['first_name'],request.POST['last_name'], request.POST['password'], request.POST['passwordconfirm'])
    if not values_of_validations["sameemail"]:
        messages.error(request,"Opps! Looks like this email already exists in our database!")
    else:
        if values_of_validations['status']:
            request.session["userId"] = values_of_validations['data'].id
            return redirect('/success')
        else:
            for err in values_of_validations['data']:
                messages.error(request, err)
            return redirect('/')

def success(request):
    if 'userId' in request.session:
        userId = request.session["userId"]
        user = User.userManager.get(id = userId)
            
        context = {
            "user": user
        }
        return render(request, 'loginreg/success.html', context)

    return redirect('/')




