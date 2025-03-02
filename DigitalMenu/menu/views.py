from django.shortcuts import render

# Create your views here.

def home(req):
    return render(req,'menu_home.html')

def plate(req):
    return render(req,'menu_plate.html')

def order(req):
    return render(req,'menu_order.html')

def help(req):
    return render(req,'menu_plate.html')