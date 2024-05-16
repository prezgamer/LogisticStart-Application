from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def logistichome(request):
    return render(request, 'logisticstart/home.html') #return logisticstart/templates/logisticstart/home.html

def logisticstart(request):
    return render(request, 'logisticstart/form.html') #return logisticstart/templates/logisticstart/form.html

def logisticlogin(request):
    return render(request, 'logisticstart/login.html') #return logisticstart/templates/logisticstart/login.html