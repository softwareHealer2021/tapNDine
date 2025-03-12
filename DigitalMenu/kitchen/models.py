from django.db import models
# from menu.models import Session
import datetime
# Create your models here.
class Order(models.Model):
    id = models.AutoField().primary_key
    table = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    status = models.CharField(max_length=10,default='in queue')
    date = models.DateField(auto_now_add=True)
    month = models.CharField(max_length=10,default=0)
    year = models.IntegerField(default=0)


class OrderItem(models.Model):
    item = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)

class Queue(models.Model):
    order_id = models.IntegerField(default=0)

class Processing(models.Model):
    order_id = models.IntegerField(default=0)

class Bill(models.Model):
    order_id = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)

