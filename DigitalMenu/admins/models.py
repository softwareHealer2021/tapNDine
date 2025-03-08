from django.db import models

# Create your models here.
class Panels(models.Model):
    user = models.CharField(max_length=25,null=True)
    upass = models.CharField(max_length=50)

class Admin(models.Model):
    admin = models.CharField(max_length=25).primary_key
    password = models.CharField(max_length=50)

class Metrics(models.Model):
    orders = models.IntegerField(default=0)
    panels = models.IntegerField(default=0)
    items = models.IntegerField(default=0)
    earnings = models.IntegerField(default=0)