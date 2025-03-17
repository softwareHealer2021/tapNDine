from django.shortcuts import render
from .models import Categories,Items
from kitchen.models import Order,OrderItem
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
    if not 't' in req.GET:
        return render(req,'menu_order.html')
    table = int(req.GET.get('t'))
    order_id = int(req.GET.get('o'))
    order = Order.objects.get(table=table,id=order_id)
    order_items = OrderItem.objects.filter(order=order.id)
    data = {
        'order':{},
        'items':[]
    }
    data['order']['amount'] = order.amount
    for x in order_items:
        item = Items.objects.get(id=x.item)
        data['items'].append({
            "name":item.name,
            "qty":x.quantity,
            "url":item.image.url,
            "wt":item.ptime
        })
    return render(req,'menu_order.html',data)

def help(req):
    return render(req,'menu_plate.html')