from django.shortcuts import render
from .models import Categories,Items
from kitchen.models import Order,OrderItem,Queue1,Queue5,Queue10,Queue15
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
        wt = 0
        match item.ptime:
            case 1:
                wt = item.ptime + (1 * min(1,Queue1.objects.count()))
            case 5:
                wt = item.ptime + (1 * min(1,Queue5.objects.count()))
            case 10:
                wt = item.ptime + (1 * min(1,Queue10.objects.count()))
            case 15:
                wt = item.ptime + (1 * min(1,Queue15.objects.count()))
        data['items'].append({
            "name":item.name,
            "qty":x.quantity,
            "url":item.image.url,
            "wt":wt
        })
    return render(req,'menu_order.html',data)

def help(req):
    return render(req,'menu_plate.html')