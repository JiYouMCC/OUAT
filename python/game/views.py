from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import ElementCard, EndingCard
import logging

def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def cards(request):
    template = loader.get_template('cards.html')
    context = {
        'element_cards': ElementCard.objects.all(),
        'ending_cards':EndingCard.objects.all()
    }
    return HttpResponse(template.render(context, request))

# 用户列表
def users(request):
    pass

# 用户
def user(reqeust):
    pass

# 游戏列表
def games(request):
    pass

# 游戏记录
def game(request):
    pass
