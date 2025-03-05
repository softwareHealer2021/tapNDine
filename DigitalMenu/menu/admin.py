from django.contrib import admin
from menu.models import *
# Register your models here.
admin.site.register(Items)
admin.site.register(Specials)
admin.site.register([Tables,Categories])