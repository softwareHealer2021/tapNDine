from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register([Order,OrderItem,Queue1,Queue10,Queue5,Queue15,Processing1,Processing5,Processing10,Processing15,Bill])