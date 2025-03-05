from django.db import models

# Create your models here.
class Items(models.Model):
    id = models.AutoField().primary_key
    name = models.CharField(max_length=25)
    description = models.TextField()
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/items',null=True)
    category = models.CharField(max_length=25)

class Specials(models.Model):
    day = models.CharField(choices=[('sunday','Sunday'),
                                    ('monday','Monday'),
                                    ('tuesday','Tuesday'),
                                    ('wednesday','Wednesday'),
                                    ('thursday','Thursday'),
                                    ('friday','Friday'),
                                    ('saturday','Saturday')],max_length=9)
    name = models.CharField(max_length=25)
    price = models.IntegerField(default=0)
    image = models.ImageField(null=True)

class Categories(models.Model):
    category = models.CharField(max_length=25)


class Tables(models.Model):
    id = models.AutoField().primary_key

#future enhancements
# class Session(models.Model):
    # table = models.IntegerField(default=0)







