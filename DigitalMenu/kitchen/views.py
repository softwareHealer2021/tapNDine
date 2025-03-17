import datetime

from django.shortcuts import render,redirect
from django.db.models import Sum, Count
from .models import Order,OrderItem,Queue,Processing,Bill
from kitchen.models import Order  
from django.utils import timezone
from admins.models import Panels
from menu.models import Items,Tables
from django.http import HttpResponse

# Create your views here.
def home(req):
    if not 'panel_user' in req.session:
        return redirect('/')
    queue = Queue.objects.values('order_id')
    queue = list(queue)
    if not queue:
        return render(req,'kitchen.html')
    queue.reverse()
    data = {
        'queue':[],
        "current":[],
    }
    if not len(Processing.objects.all()):
        live = queue.pop()
        Queue.objects.filter(order_id=live['order_id']).delete()
        current=Processing(order_id=live['order_id'])
        order_obj = Order.objects.get(id=current.order_id)
        order_obj.status = "processing"
        order_obj.save()
        current.save()
        data["current_table"] = Order(id=current.order_id).table
        data["current_id"] = current.order_id
        print(Order(id=current.order_id).table)
    else:
        current = Processing.objects.all()
        current = current[0]
        data["current_table"] = Order.objects.get(id=current.order_id).table
        data["current_id"] = current.order_id

    data["orders"]=len(queue)
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
    else:
        return redirect('/kitchen')
    return HttpResponse("")

def complete_order(req):
    if Processing.objects.all():
        order_id = Processing.objects.all()[0].order_id
        order_obj = Order.objects.get(id=order_id)
        order_obj.status = "completed"
        order_obj.save()
        Processing.objects.all().delete()
    else:
        return redirect('/kitchen')
    return HttpResponse("Success")

def logout(req):
    del req.session['panel_user']
    return redirect('/')