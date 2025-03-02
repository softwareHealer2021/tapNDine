from django.db import models

# Create your models here.
class Order(models.Model):
    id = models.IntegerField
    session = models.IntegerField
    amount = models.IntegerField
    status = models.CharField
    date = models.DateField

class OrderItem(models.Model):
    item = models.IntegerField
    order = models.IntegerField
    quantity = models.IntegerField

class Bill(models.Model):
    pass

