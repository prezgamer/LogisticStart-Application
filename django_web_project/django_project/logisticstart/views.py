from django.shortcuts import render,redirect 
from django.contrib.auth import authenticate, login, logout
from .models import NewListing
from .forms import SignupForm, LoginForm, CreateListingForm
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
def logistichome(request):
    return render(request, 'logisticstart/home.html') #return logisticstart/templates/logisticstart/home.html

def logisticform(request): #return logisticstart/templates/logisticstart/form.html
    if request.method == 'POST':
        form = CreateListingForm(request.POST)
        if form.is_valid():
            form.save()
            items = NewListing.objects.all()
            return render(request, 'logisticstart/items_list.html', {'items': items})
    else:
        form = CreateListingForm()
        return render(request, 'logisticstart/form.html', {'form': form})

def logisticitems_list(request):
    items = NewListing.objects.all()
    return render(request, 'logisticstart/items_list.html', {'items': items})

# signup page
def logisticsignup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('logisticstart-login')
    else:
        form = SignupForm()
    return render(request, 'logisticstart/signup.html', {'form': form})

# login page
def logisticlogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('logisticstart-test')
    else:
        form = LoginForm()
    return render(request, 'logisticstart/login.html', {'form': form})

def logisticdashboard(request):
    distinct_senders = NewListing.objects.values('sender_name').distinct()
    distinct_types = NewListing.objects.values('item_type').distinct()
    total_listing = NewListing.objects.count()
    
    dashboard ={
        'distinct_senders': distinct_senders,
        'distinct_types' : distinct_types,
        'total_listing' : total_listing
    }
    
    return render(request, 'logisticstart/dashboard.html', dashboard)

def logistictest(request):
    return render(request, 'logisticstart/test.html')
    
def custom_page_not_found_view(request, exception):
    return render(request, "errors/404.html", {})

def custom_error_view(request, exception=None):
    return render(request, "errors/500.html", {})

def custom_permission_denied_view(request, exception=None):
    return render(request, "errors/403.html", {})

def custom_bad_request_view(request, exception=None):
    return render(request, "errors/400.html", {})


# Edit listing view
def edit_listing(request, pk):
    listing = get_object_or_404(NewListing, pk=pk)
    if request.method == 'POST':
        form = CreateListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('logisticitems_list')  # Adjust this redirect as necessary
    else:
        form = CreateListingForm(instance=listing)
    return render(request, 'logisticstart/edit_listing.html', {'form': form})