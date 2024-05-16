from django.urls import path
from . import views

urlpatterns = [
    path('', views.logistichome, name='logisticstart-home'), #look for logistichome function
    path('form/', views.logisticstart, name='logisticstart-startform'), #look for logisticstart function
    path('login/', views.logisticlogin, name='logisticlogin-login'), #look for logisticlogin function
]