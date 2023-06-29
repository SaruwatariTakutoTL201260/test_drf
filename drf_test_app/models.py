from django.db import models
from django.utils import timezone 

class TableWare(models.Model):
    contents = models.TextField()
    is_deleted = models.BooleanField(default=False);

class Dish(models.Model):
    table_id = models.ForeignKey(TableWare,  related_name='dishes', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    modified = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False);

class User(models.Model):
    name = models.CharField(max_length=64);
    
# Create your models here.
