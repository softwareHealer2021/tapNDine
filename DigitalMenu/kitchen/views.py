import datetime

from django.shortcuts import render,redirect
from django.db.models import Sum, Count
from .models import Order,OrderItem,Queue1,Queue5,Queue10,Queue15,Processing1,Processing5,Processing10,Processing15,Bill
from kitchen.models import Order  
from django.utils import timezone
from admins.models import Panels
from menu.models import Items,Tables
from django.http import HttpResponse

# Create your views here.
def home(req):
    if not 'panel_user' in req.session:
        return redirect('/')
    queue1 = list(Queue1.objects.all())
    queue2 = list(Queue1.objects.all())
    queue3 = list(Queue1.objects.all())
    queue4 = list(Queue1.objects.all())
    print(queue1,queue2,queue3,queue4)
    data = {
        'queue1':[],
        'queue5':[],
        'queue10':[],
        'queue15':[],
        "current1":[],
        "current5":[],
        "current10":[],
        "current15":[],
    }

    return render(req,'kitchen.html')

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
            time = item.ptime
            match time:
                case 1:
                    Queue1(order_id=order_id,table=table,item_id=item.id).save()
                case 5:
                    Queue5(order_id=order_id,table=table,item_id=item.id).save()
                case 10:
                    Queue10(order_id=order_id,table=table,item_id=item.id).save()
                case 15:
                    Queue15(order_id=order_id,table=table,item_id=item.id).save()
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