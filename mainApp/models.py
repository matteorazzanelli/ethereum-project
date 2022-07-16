
from djongo import models

from djongo.models.fields import ObjectIdField
  
class Event(models.Model):
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
  description = models.CharField()
  amount = models.FloatField()
  deadline = models.DateTimeField(auto_now_add=True)
  
  status = models.CharField(choices=STATUS, default='pending')
  type = models.CharField(choices=TYPE)