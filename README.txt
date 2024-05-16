1. Download Python
2. Download Django (python -m pip install Django)

To Create a new webpage:
1. Write new function in logisticstart/views.py, follow steps from there

Example: 
def logisticlogin(request):
    return render(request, 'logisticstart/login.html') #return logisticstart/templates/logisticstart/login.html

2. Write new html code in the logisticstart/templates/logisticstart as nameoffile.html
3. Replace name with appropriate name for the logisticstart/views.py
4. Write new webpage source in logisticstart/urls.py

Example:
path('newpage/', views.functionname, name='functionname-type'), 