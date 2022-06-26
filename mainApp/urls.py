from django.urls import path
from . import views

app_name = 'mainApp'

urlpatterns = [
  # app
  path('', views.homepage, name="homepage"),
]    