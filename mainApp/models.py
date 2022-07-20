
from djongo import models

from djongo.models.fields import ObjectIdField

from django_ethereum.fields import EthereumAddressField
  
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
  id = models.FloatField(blank=True, default=0)
  buyer = EthereumAddressField(blank=True, default='0x0000000000000000000000000000000000000000')
  seller = EthereumAddressField(blank=True, default='0x0000000000000000000000000000000000000000')
  description = models.CharField(blank=True, max_length=500, default=' ')
  amount = models.FloatField(blank=True, default=0)
  amount_for_now = models.FloatField()
  deadline = models.IntegerField(blank=True, default=2)
  
  status = models.CharField(max_length=50, choices=STATUS, default='pending')
  type = models.CharField(max_length=50, choices=TYPE)
  
class Event(models.Model):
  _id = models.ObjectIdField()
  type = models.CharField(max_length=50)
  times = models.IntegerField(default=0)
  date = models.DateTimeField(auto_now_add=True)