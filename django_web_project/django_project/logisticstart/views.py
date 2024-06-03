from django.shortcuts import render,redirect 
from django.contrib.auth import authenticate, login, logout
from .models import NewItemListing, NewWarehouseListing, NewWorkerListing
from .forms import SignupForm, LoginForm, CreateItemListingForm, CreateWarehouseListingForm, CreateWorkerListingForm
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
def logistichome(request):
    return render(request, 'logisticstart/home.html') #return logisticstart/templates/logisticstart/home.html

def logisticitems_list(request):
    items = NewItemListing.objects.all()
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

# logistic warehouse item form (Will need to update this)
def logisticWarehouseItemForm(request, id):
    warehouse = get_object_or_404(NewWarehouseListing, id=id)
    if request.method == 'POST':
        form = CreateItemListingForm(request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.warehouse = warehouse  
            new_item.save()
            return redirect('logisticstart-warehouseitemlist', id=warehouse.id)
    else:
        form = CreateItemListingForm()
    return render(request, 'logisticstart/WarehouseItems/warehouseitemlistform.html', {'form': form, 'warehouse': warehouse})
    
# logistic warehouse list
def logisticWarehouseList(request):
    warehouses = NewWarehouseListing.objects.all()
    return render(request, 'logisticstart/Warehouse/warehouseList.html', {'warehouses': warehouses})

def warehouse_item_list(request, id):
    warehouse = get_object_or_404(NewWarehouseListing, id=id)
    items = warehouse.items.all()
    return render(request, 'logisticstart/WarehouseItems/warehouseitemlist.html', {'warehouse': warehouse, 'items': items})

# new worker page
def logisticNewWorker(request):
    if request.method == 'POST':
        form = CreateWorkerListingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('logisticstart-newworker')
    else:
        form = CreateWorkerListingForm()
    return render(request, 'logisticstart/Worker/new_worker.html', {'form': form})

def add_warehouse(request):
    if request.method == 'POST':
        form = CreateWarehouseListingForm(request.POST)
        if form.is_valid():
            form.save()
            warehouses = NewWarehouseListing.objects.all()
            return render(request, 'logisticstart/Warehouse/warehouseList.html', {'warehouses': warehouses})
    else:
        form = CreateWarehouseListingForm()
    return render(request, 'logisticstart/Warehouse/add_warehouse.html', {'form': form})

def warehouse_list(request):
    warehouses = NewWarehouseListing.objects.all()
    return render(request, 'logisticstart/Warehouse/warehouseList.html', {'warehouses': warehouses})

# Edit listing view 
def edit_listing(request, pk):
    listing = get_object_or_404(NewItemListing, pk=pk)
    if request.method == 'POST':
        form = CreateItemListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('logisticstart-list')  # Adjust this redirect as necessary
    else:
        form = CreateItemListingForm(instance=listing)
    return render(request, 'logisticstart/edit_listing.html', {'form': form})

def custom_page_not_found_view(request, exception):
    return render(request, "errors/404.html", {})

def custom_error_view(request, exception=None):
    return render(request, "errors/500.html", {})

def custom_permission_denied_view(request, exception=None):
    return render(request, "errors/403.html", {})

def custom_bad_request_view(request, exception=None):
    return render(request, "errors/400.html", {})

#Dashboard
def logisticdashboard(request):
    
    #Queries
    workers = NewWorkerListing.objects.all().values('id', 'worker_name', 'worker_phonenumber')
    warehouses = NewWarehouseListing.objects.all().values('warehouse_name', 'warehouse_postalcode', 'warehouse_phonenumber')
    
    dashboard = {
        'warehouses': warehouses,
        'workers': workers
    }
    return render(request, 'logisticstart/dashboard.html', dashboard)
