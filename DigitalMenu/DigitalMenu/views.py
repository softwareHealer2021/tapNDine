from django.shortcuts import render, redirect,reverse
from admins.views import admin_login
from admins.models import Panels
from kitchen.views import home

def login(req):
    data = {}
    if 'login' in req.session:
        data = {'failure':True}
        del req.session['login']
    return render(req,'login.html',data)

def login_auth(req):
    if req.method == 'POST':
        id = req.POST.get('email')
        password = req.POST.get('password')
        check = req.POST.get('check')
        if check:
            if admin_login(req,id,password):
                req.session['admin_user'] = 'admin'
                return redirect('admin-home')
            else:
                req.session['login'] = 'unsuccessful'
                return redirect('/')
        else:
            obj = Panels.objects.filter(user=id,upass=password)
            if obj:
                req.session['panel_user'] = 'panel'
                return redirect('kitchen-home')
            else:
                req.session['login'] = 'unsuccessful'
                return redirect('/')
    return render(req,'login.html')