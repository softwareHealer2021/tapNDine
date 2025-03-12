from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from kitchen.models import Order
from menu.models import Items
from .models import Panels
from django.shortcuts import render, redirect
import json
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import datetime
# Create your views here.
def admin_render(req):
   
    current_year = datetime.datetime.now().year
    last_year = current_year - 1
    

    all_orders = Order.objects.all()
    
 
    current_year_orders = all_orders.filter(year=current_year)
    previous_year_orders = all_orders.filter(year=last_year)
    

    total_orders = len(current_year_orders)
    total_earnings = sum(order.amount for order in current_year_orders)
    total_panels = len(Panels.objects.all())
    total_items = len(Items.objects.all())
    
  
    previous_year_order_count = len(previous_year_orders)
    previous_year_earnings = sum(order.amount for order in previous_year_orders)
    

    previous_year_panels = total_panels
    previous_year_items = total_items
    
    monthly_data = {
        str(current_year): [0] * 12,
        str(last_year): [0] * 12
    }
    

    for order in current_year_orders:
     
        month_idx = get_month_index(order.month)
        if 0 <= month_idx < 12:
            monthly_data[str(current_year)][month_idx] += order.amount
    

    for order in previous_year_orders:
        month_idx = get_month_index(order.month)
        if 0 <= month_idx < 12:
            monthly_data[str(last_year)][month_idx] += order.amount
    
    if not Metrics.objects.exists() or len(all_orders) != Metrics.objects.first().orders:
        if Metrics.objects.exists():
            metrics = Metrics.objects.first()
            metrics.orders = len(all_orders)
            metrics.earnings = sum(order.amount for order in all_orders)
            metrics.panels = total_panels
            metrics.items = total_items
            metrics.save()
        else:
            Metrics(
                orders=len(all_orders),
                panels=total_panels,
                items=total_items,
                earnings=sum(order.amount for order in all_orders)
            ).save()
    

    panels = Panels.objects.all()
    panel_data = [{'user': p.user, 'pass': p.upass} for p in panels]
    
    data = {
        'total_orders': total_orders,
        'total_items': total_items,
        'total_panels': total_panels,
        'total_earnings': total_earnings,
        'panels': panel_data,
        'current_year': current_year,
        'last_year': last_year,
        'monthly_data': json.dumps(monthly_data),
        'previous_year_orders': previous_year_order_count,
        'previous_year_items': previous_year_items,
        'previous_year_panels': previous_year_panels
    }
    
    return render(req, 'admin_template.html', data)

def get_month_index(month):
    """Convert month to index (0-11)"""
    if isinstance(month, int) and 1 <= month <= 12:
        return month - 1
    
    month_names = [
        "jan", "feb", "mar", "apr", "may", "jun", 
        "jul", "aug", "sep", "oct", "nov", "dec"
    ]
    
    if isinstance(month, str):
        month_str = month.lower()[:3]  # First 3 chars of month name
        if month_str in month_names:
            return month_names.index(month_str)
    
    # Default to current month if invalid
    return datetime.datetime.now().month - 1
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

def admin_login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            panel_user = Panels.objects.get(user=username)
            
            if panel_user.upass == password:
                request.session['admin_user'] = username
                
           
                return redirect('/admin/') 
            else:
                return render(request, 'admin_login.html', {
                    'error': 'Invalid password. Please try again.'
                })
        except Panels.DoesNotExist:
            return render(request, 'admin_login.html', {
                'error': 'User not found.'
            })

    return render(request, 'admin_login.html')