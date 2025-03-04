from django.shortcuts import render
from .models import Order
from menu.models import Session,Items,Tables
# Create your views here.
def home(req):
    return render(req,'kitchen.html')

def order(req):
    import json
    from django.http import HttpResponse
    products = req.body.decode()
    if products:
        products = json.loads(products)
    if products:
        Session(table=Tables.objects.get(id=1)).save()
        session = Session.objects.get(table=1)
        amount = 0
        for x in products:
            item = Items.objects.filter(id=x['id'])
            amount += (item.price*x.qty)
        # Order(session=session, amount=amount,)
        return HttpResponse("Success")