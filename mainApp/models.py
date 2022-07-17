
from djongo import models

from djongo.models.fields import ObjectIdField
  
class NotaryModelForm(models.Model):
  _id = ObjectIdField()
  TYPE = [
    ('new', 'new'),
    ('contribute', 'contribute'),
    ('delete', 'delete'),
  ]
  STATUS = [
    ('pending', 'pending'),
    ('closed', 'closed'),
  ]
  id = models.FloatField()
  buyer = models.BinaryField(editable=True)
  seller = models.BinaryField(editable=True)
  description = models.CharField(max_length=500)
  amount = models.FloatField()
  deadline = models.IntegerField(editable=True)
  
  status = models.CharField(max_length=50, choices=STATUS, default='pending')
  type = models.CharField(max_length=50, choices=TYPE)
  
class Event(models.Model):
  _id = models.ObjectIdField()
  type = models.CharField(max_length=50)
  times = models.IntegerField(default=0)
  date = models.DateTimeField(auto_now_add=True)