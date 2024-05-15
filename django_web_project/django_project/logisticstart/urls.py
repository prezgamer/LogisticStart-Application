from django.urls import path
from . import views

urlpatterns = [
    path('', views.logisticstart, name='logisticstart-home'),
]