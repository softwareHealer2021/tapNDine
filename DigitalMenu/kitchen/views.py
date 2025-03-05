from django.shortcuts import render
from .models import Order,OrderItem,Queue,Processing,Bill
from admins.models import Panels
from menu.models import Items,Tables
# Create your views here.
def home(req):
    queue = Queue.objects.values('order_id')
    queue = list(queue)
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

    }
    return render(req,'kitchen.html')

def order(req):
    import json
    from django.http import HttpResponse
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
        order = Order(table=table, amount=amount)
        order.save()
        order_id = order.id
        for x in products['plate']:
            item = Items.objects.get(id=x['id'])
            OrderItem(item= item.id,order = order.id,quantity = x['qty']).save()
        Queue(order_id=order.id).save()
        return HttpResponse(order_id)
    return HttpResponse("")