from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required

def index(request):
    template = loader.get_template('index.html')
    context  = {}
    return HttpResponse(template.render(context, request))


def login(request, user, password):
    pass

def logout(request):
    pass

def register(request, user, password, email):
    pass

