import datetime

from django.shortcuts import render
from django.db.models import Sum, Count
from .models import Order,OrderItem,Queue,Processing,Bill
from kitchen.models import Order  
from django.utils import timezone
from admins.models import Panels
from menu.models import Items,Tables
from django.http import HttpResponse

# Create your views here.
def home(req):
    queue = Queue.objects.values('order_id')
    queue = list(queue)
    if not queue:
        return render(req,'kitchen.html')
    queue.reverse()
    if not len(Processing.objects.all()):
        live = queue.pop()
        Queue.objects.filter(order_id=live['order_id']).delete()
        current=Processing(order_id=live['order_id'])
        current.save()
    else:
        current = Processing.objects.all()
        current = current[0]
    data = {
        'queue':[],
        "current":[],
        "current_table":Order(id=current.order_id).table,
        "current_id":current.order_id,
        "orders":len(queue),
    }
    for x in queue:
        items = len(OrderItem.objects.filter(order=x['order_id']))
        table = Order.objects.get(id=x['order_id']).table
        data['queue'].append({
            'id':x['order_id'],
            'count':items,
            'table':table,
        })
    order_items = OrderItem.objects.filter(order=current.order_id)
    for x in order_items:
        item = Items.objects.get(id=x.item)
        data['current'].append({
            'name':item.name,
            'url':item.image.url,
        })
    return render(req,'kitchen.html',data)

def order(req):
    import json
    products = req.body.decode()
    if products:
        products = json.loads(products)
        # Session(table=products['table']).save()
        # session = Session.objects.get(table=products['table'])
        table = products['table']
        amount = 0
        for x in products['plate']:
            item = Items.objects.get(id=x['id'])
            amount += (item.price*x['qty'])
        month = datetime.datetime.now().strftime('%b')  
        year = datetime.datetime.now().year
        order = Order(table=table, amount=amount,month=month,year=year)
        order.save()
        order_id = order.id
        for x in products['plate']:
            item = Items.objects.get(id=x['id'])
            OrderItem(item= item.id,order = order.id,quantity = x['qty']).save()
        Queue(order_id=order.id).save()
        return HttpResponse(order_id)
    return HttpResponse("")

def complete_order(req):
    Processing.objects.all().delete()
    return HttpResponse("Success")