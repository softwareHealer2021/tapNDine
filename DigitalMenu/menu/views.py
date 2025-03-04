from django.shortcuts import render
from .models import Categories
# Create your views here.

def home(req):
    data = {
        'categories':[],
    }
    return render(req,'menu_home.html',data)

def plate(req):
    return render(req,'menu_plate.html')

def order(req):
    return render(req,'menu_order.html')

def help(req):
    return render(req,'menu_plate.html')