from django import forms
from .models import NotaryModelForm

class NotaryForm(forms.ModelForm):
  class Meta:
    model = NotaryModelForm
    fields = ('id','type','buyer','seller','description','amount','deadline')

