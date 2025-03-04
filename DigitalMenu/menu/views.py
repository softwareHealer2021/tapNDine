from django.shortcuts import render
from .models import Categories,Items
# Create your views here.

def home(req):
    data = {
        'categories':[],
        'items':[],
    }
    for x in Categories.objects.all():
        data['categories'].append(x.category)

    for x in Items.objects.all():
        data['items'].append(
            {
                'id':x.id,
                "item":x.name,
                "description":x.description,
                "price":x.price,
                "url":x.image.url,
                "category":x.category,

            })
    return render(req,'menu_home.html',data)


def plate(req):
    data = {
        'items': [],
    }

    for x in Items.objects.all():
        data['items'].append(
            {
                'id': x.id,
                "item": x.name,
                "description": x.description,
                "price": x.price,
                "url": x.image.url,
                "category": x.category,
            })
    return render(req,'menu_plate.html',data)

def order(req):
    return render(req,'menu_order.html')

def help(req):
    return render(req,'menu_plate.html')