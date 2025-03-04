from django.db import models
from menu.models import Session

# Create your models here.
class Order(models.Model):
    id = models.AutoField().primary_key
    session = models.ForeignKey(Session,on_delete=models.SET_NULL,null=True)
    amount = models.IntegerField
    status = models.CharField
    date = models.DateField

class OrderItem(models.Model):
    item = models.IntegerField
    order = models.IntegerField
    quantity = models.IntegerField

class Queue(models.Model):
    order_id = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)

class Processing(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)

class Bill(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    amount = models.IntegerField()

