from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from kitchen.models import Order
from menu.models import Items
import json
# Create your views here.
def admin_render(req):
    orders = earnings = panels = items = 0
    if (not len(Metrics.objects.all())) or len(Order.objects.all()) != Metrics.objects.all()[0].orders:
        orders = len(Order.objects.all())
        earnings = sum([x['amount'] for x in list(Order.objects.all().values('amount'))])
        panels = len(Panels.objects.all())
        items = len(Items.objects.all())
        Metrics(orders=orders,panels=panels,items=items,earnings=earnings).save()
    panels = Panels.objects.all()
    metrics = Metrics.objects.all()[0]
    data={
        'total_orders':metrics.orders,
        'total_items':metrics.items,
        'total_panels':metrics.panels,
        'total_earnings':metrics.earnings,
        'panels':[]
    }
    for x in panels:
        data['panels'].append({
            'user':x.user,
            'pass':x.upass,
        })
    return render(req,'admin_template.html',data)


def admin_add_staff(req):
    panel = req.body.decode()
    panel = json.loads(panel)
    Panels(user=panel['email'],upass=panel['password']).save()
    return HttpResponse("Success")

def admin_delete_panel(req):
    panel = req.body.decode()
    panel = json.loads(panel)
    Panels.objects.get(user=panel['panel']).delete()
    return HttpResponse("Success")