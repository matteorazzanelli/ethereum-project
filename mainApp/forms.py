from django import forms
from .models import Event

class NotaryForm(forms.ModelForm):
  class Meta:
    model = Event
    fields = ('id','type','buyer','seller','description','amount','deadine')

