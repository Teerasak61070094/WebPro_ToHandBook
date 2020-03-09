from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)
    name_book = models.CharField(max_length=50)
    type_for = (('S', 'ขาย'),('B', 'ซื้อ'))
    type_post = models.CharField(max_length=1, choices=type_for)
    price = models.FloatField(default=0)
    picture = models.URLField(max_length = 500,null = True) 
    status = models.BooleanField(default=True) 


