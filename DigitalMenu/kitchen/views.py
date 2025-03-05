from django.shortcuts import render
from .models import Order,OrderItem,Queue,Processing,Bill
from menu.models import Session,Items,Tables
# Create your views here.
def home(req):
    queue = list(Queue.objects.all())
    print(queue)
    return render(req,'kitchen.html')

def order(req):
    import json
    from django.http import HttpResponse
    products = req.body.decode()
    if products:
        products = json.loads(products)
        Session(table=6).save()
        session = Session.objects.get(table=2)
        amount = 0
        for x in products:
            item = Items.objects.get(id=x['id'])
            amount += (item.price*x['qty'])
        order = Order(session=session.table, amount=amount)
        order.save()
        for x in products:
            item = Items.objects.get(id=x['id'])
            OrderItem(item= item.id,order = order.id,quantity = x['qty'])
        Queue(order_id=order.id).save()
        return HttpResponse("Success")