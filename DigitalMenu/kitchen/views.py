import datetime
import json
from django.shortcuts import render,redirect
from django.db.models import Sum, Count
from .models import Order,OrderItem,Queue1,Queue5,Queue10,Queue15,Processing1,Processing5,Processing10,Processing15,Bill
from kitchen.models import Order  
from django.utils import timezone
from admins.models import Panels
from menu.models import Items,Tables
from django.http import HttpResponse,JsonResponse

# Create your views here.
def home(req):
    if not 'panel_user' in req.session:
        return redirect('/')
    queue1 = []
    queue5 = []
    queue10 = []
    queue15 = []
    data = {
        "current1":{},
        "current5":{},
        "current10":{},
        "current15":{},
    }
    order_items = []
    current = None
    if len(Queue1.objects.all()):
        for x in list(Queue1.objects.all()):
            queue1.append({"order_id":x.order_id,"table_id":x.table_id,"item_id":x.item_id,})
        queue1 = sorted(queue1, key=lambda x: x['order_id'],reverse=True)
    if not len(Processing1.objects.all()):
        if queue1:
            live = queue1.pop()
            Queue1.objects.filter(order_id=live['order_id'],item_id=live['item_id'],table_id=live['table_id']).delete()
            current=Processing1(order_id=live['order_id'],item_id=live['item_id'],table_id=live['table_id'])
            order_obj = Order.objects.get(id=current.order_id)
            current.save()
            data["current1_id"] = current.order_id
            data["current1_table"] = current.table_id
            order_items.append(current.item_id)
    else:
        current = Processing1.objects.all()[0]
        data["current1_table"] = current.table_id
        data["current1_id"] = current.order_id
        order_items.append(current.item_id)
    if len(Processing1.objects.all()):
        data['current1'] = {
            "url": Items.objects.get(id=order_items[0]).image,
            "name": Items.objects.get(id=order_items[0]).name,
            "table": Processing1.objects.all()[0].table_id
        }
    else:
        order_items.append(0)
    if len(Queue5.objects.all()):
        for x in list(Queue5.objects.all()):
            queue5.append({"order_id":x.order_id,"table_id":x.table_id,"item_id":x.item_id,})
        queue5 = sorted(queue5, key=lambda x: x['order_id'],reverse=True)
    if not len(Processing5.objects.all()):
        if queue5:
            live = queue5.pop()
            Queue5.objects.filter(order_id=live['order_id'],item_id=live['item_id'],table_id=live['table_id']).delete()
            current=Processing5(order_id=live['order_id'],item_id=live['item_id'],table_id=live['table_id'])
            order_obj = Order.objects.get(id=current.order_id)
            current.save()
            data["current5_id"] = current.order_id
            data["current5_table"] = current.table_id
            order_items.append(current.item_id)
    else:
        current = Processing5.objects.all()[0]
        data["current5_id"] = current.order_id
        data["current5_table"] = current.table_id
        order_items.append(current.item_id)
    if len(Processing5.objects.all()):
        data['current5'] = {
            "url": Items.objects.get(id=order_items[1]).image,
            "name": Items.objects.get(id=order_items[1]).name,
            "table": Processing5.objects.all()[0].table_id
        }
    else:
        order_items.append(0)
    if len(Queue10.objects.all()):
        for x in list(Queue10.objects.all()):
            queue10.append({"order_id":x.order_id,"table_id":x.table_id,"item_id":x.item_id,})
        queue10 = sorted(queue10, key=lambda x: x['order_id'],reverse=True)
    if not len(Processing10.objects.all()):
        if queue10:
            live = queue10.pop()
            Queue10.objects.filter(order_id=live['order_id'],item_id=live['item_id'],table_id=live['table_id']).delete()
            current=Processing10(order_id=live['order_id'],item_id=live['item_id'],table_id=live['table_id'])
            order_obj = Order.objects.get(id=current.order_id)
            current.save()
            data["current10_id"] = current.order_id
            data["current10_table"] = current.table_id
            order_items.append(current.item_id)
    else:
        current = Processing10.objects.all()[0]
        data["current10_id"] = current.order_id
        data["current10_table"] = current.table_id
        order_items.append(current.item_id)
    if len(Processing10.objects.all()):
        data['current10'] = {
            "url": Items.objects.get(id=order_items[2]).image,
            "name": Items.objects.get(id=order_items[2]).name,
            "table": Processing10.objects.all()[0].table_id
        }
    else:
        order_items.append(0)
    if len(Queue15.objects.all()):
        for x in list(Queue15.objects.all()):
            queue15.append({"order_id":x.order_id,"table_id":x.table_id,"item_id":x.item_id,})
        queue15 = sorted(queue15, key=lambda x: x['order_id'],reverse=True)
    if not len(Processing15.objects.all()):
        if queue15:
            live = queue15.pop()
            Queue15.objects.filter(order_id=live['order_id'],item_id=live['item_id'],table_id=live['table_id']).delete()
            current=Processing15(order_id=live['order_id'],item_id=live['item_id'],table_id=live['table_id'])
            order_obj = Order.objects.get(id=current.order_id)
            current.save()
            data["current15_id"] = current.order_id
            data["current15_table"] = current.table_id
            order_items.append(current.item_id)
    else:
        current = Processing15.objects.all()[0]
        data["current15_id"] = current.order_id
        data["current15_table"] = current.table_id
        order_items.append(current.item_id)
    if len(Processing15.objects.all()):
        data['current15'] = {
            "url":Items.objects.get(id=order_items[3]).image,
            "name":Items.objects.get(id=order_items[3]).name,
            "table":Processing15.objects.all()[0].table_id
        }
    else:
        order_items.append(0)
    data["orders"]=(len(queue1)+len(queue5)+len(queue10)+len(queue15))
    return render(req,'kitchen.html',data)

def order(req):
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
                    Queue1(order_id=order_id,table_id=table,item_id=item.id).save()
                case 5:
                    Queue5(order_id=order_id,table_id=table,item_id=item.id).save()
                case 10:
                    Queue10(order_id=order_id,table_id=table,item_id=item.id).save()
                case 15:
                    Queue15(order_id=order_id,table_id=table,item_id=item.id).save()
        return HttpResponse(order_id)
    else:
        return redirect('/kitchen')

def complete_order(request):
    Processing = request.body.decode()
    if Processing:
        section = json.loads(Processing)
        match int(section['section']):
            case 1:
                Processing1.objects.all().delete()
            case 5:
                Processing5.objects.all().delete()
            case 10:
                Processing10.objects.all().delete()
            case 15:
                Processing15.objects.all().delete()
    else:
        return redirect('/kitchen')
    return HttpResponse("Success")

def logout(req):
    del req.session['panel_user']
    return redirect('/')