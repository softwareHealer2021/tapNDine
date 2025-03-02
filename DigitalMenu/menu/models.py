from django.db import models

# Create your models here.
class Items(models.Model):
    id = models.IntegerField
    name = models.CharField
    description = models.TextField
    price = models.IntegerField
    image = models.ImageField
    category = models.CharField

class Specials(models.Model):
    day = models.CharField
    name = models.CharField
    price = models.IntegerField
    image = models.ImageField

class Session(models.Model):
    id = models.IntegerField
    table = models.IntegerField
    start = models.TimeField
    end = models.TimeField






