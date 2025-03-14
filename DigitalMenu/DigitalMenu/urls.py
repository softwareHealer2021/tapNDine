"""DigitalMenu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin as admin
from django.urls import path
from menu import views as menu
from kitchen import views as kitchen
from admins import views as admins
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admins/', admin.site.urls),
    path('menu/home', menu.home),
    path('menu/plate', menu.plate),
    path('menu/order', menu.order),
    path('menu/help', menu.help),
    path('kitchen', kitchen.home),
    path('kitchen/order', kitchen.order),
    path('kitchen/order/complete', kitchen.complete_order),
    path('admin/', admins.admin_render),
    path('admin/add_staff', admins.admin_add_staff),
    path('admin/delete_panel', admins.admin_delete_panel),
]

# ✅ Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)