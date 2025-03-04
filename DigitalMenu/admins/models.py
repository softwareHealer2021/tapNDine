from django.db import models

# Create your models here.
class Panels(models.Model):
    user = models.CharField(max_length=25).primary_key
    upass = models.CharField(max_length=50)

class Metrics(models.Model):
    orders = models.IntegerField()
    daily = models.IntegerField()
    panels = models.IntegerField()
    items = models.IntegerField()