from django.shortcuts import render

# Create your views here.
def logistichome(request):
    return render(request, 'logisticstart/home.html') #return logisticstart/templates/logisticstart/home.html

def logisticstart(request):
    return render(request, 'logisticstart/form.html') #return logisticstart/templates/logisticstart/form.html

def logisticlogin(request):
    return render(request, 'logisticstart/login.html') #return logisticstart/templates/logisticstart/login.html

def custom_page_not_found_view(request, exception):
    return render(request, "errors/404.html", {})

def custom_error_view(request, exception=None):
    return render(request, "errors/500.html", {})

def custom_permission_denied_view(request, exception=None):
    return render(request, "errors/403.html", {})

def custom_bad_request_view(request, exception=None):
    return render(request, "errors/400.html", {})