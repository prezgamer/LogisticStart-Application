from django.shortcuts import render,redirect 
from django.contrib.auth import authenticate, login, logout
from .models import NewItemListing, NewWarehouseListing, NewWorkerListing,NewDeliverySchedule
from .forms import SignupForm, LoginForm, CreateItemListingForm, CreateWarehouseListingForm, CreateWorkerListingForm,CreateDeliveryScheduleForm,register
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


# Create your views here.
def logistichome(request):
    return render(request, 'logisticstart/home.html') #return logisticstart/templates/logisticstart/home.html

def item_list(request):
    items = NewItemListing.objects.all()
    return render(request, 'logisticstart/items_list.html', {'items': items})


# logistic warehouse item form (Will need to update this)
def add_warehouse_item(request, id):
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
def add_new_worker(request):
    if request.method == 'POST':
        form = CreateWorkerListingForm(request.POST)
        if form.is_valid():
            form.save()
            worker = NewWorkerListing.objects.all()
            return render(request, 'logisticstart/Worker/worker.html', {"workers": worker})
    else:
        form = CreateWorkerListingForm()
    return render(request, 'logisticstart/Worker/new_worker.html', {'form': form})

# add warehouses
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

# warehouse list
def warehouse_list(request):
    warehouses = NewWarehouseListing.objects.all()
    return render(request, 'logisticstart/Warehouse/warehouseList.html', {'warehouses': warehouses})

# worker page
def worker_page(request):
    workers = NewWorkerListing.objects.all()
    return render(request, 'logisticstart/Worker/worker.html', {'workers': workers})

#not working
def edit_delivery_item(request, deliveryid):
    listing = get_object_or_404(NewDeliverySchedule, deliveryid=deliveryid)
    if request.method == 'POST':
        form = CreateDeliveryScheduleForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('logisticstart-delivery_schedule', deliveryid=deliveryid)
    else:
        form = CreateDeliveryScheduleForm(instance=listing)
    return render(request, 'logisticstart-edit_delivery_schedule', {'form': form})

#working
def delete_delivery_item(request, deliveryid):
    listing = get_object_or_404(NewDeliverySchedule, deliveryid=deliveryid)
    if request.method == 'POST':
        listing.delete()
        return redirect('logisticstart-delivery_schedule')
    return render(request, 'logisticstart-delete_delivery_schedule', {'listing': listing})

def edit_warehouse_item(request, id):
    listing = get_object_or_404(NewItemListing, id=id)
    if request.method == 'POST':
        form = CreateItemListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('logisticstart-warehouseitemlist', id=listing.warehouse.id) 
    else:
        form = CreateItemListingForm(instance=listing)
    return render(request, 'logisticstart/WarehouseItems/edit_warehouse_items.html', {'form': form})

def delete_warehouse_item(request, id):
    listing = get_object_or_404(NewItemListing, id=id)
    if request.method == 'POST':
        listing.delete()
        return redirect('logisticstart-warehouseitemlist', id=listing.warehouse.id)
    return render(request, 'delete_listing', {'listing': listing})

def edit_warehouse_listing(request, id):
    listing = get_object_or_404(NewWarehouseListing, id=id)
    if request.method == 'POST':
        form = CreateWarehouseListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('logisticstart-warehouselist') 
    else:
        form = CreateWarehouseListingForm(instance=listing)
    return render(request, 'logisticstart/Warehouse/edit_warehouse.html', {'form': form})

def delete_warehouse_listing(request, id):
    warehouse = get_object_or_404(NewWarehouseListing, id=id)
    if request.method == 'POST':
        warehouse.delete()
        return redirect('logisticstart-warehouselist')
    return render(request, 'delete_warehouse_listing', {'warehouse': warehouse})

def edit_worker_listing(request, id):
    listing = get_object_or_404(NewWorkerListing, id=id)
    if request.method == 'POST':
        form = CreateWorkerListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('logisticstart-worker') 
    else:
        form = CreateWorkerListingForm(instance=listing)
    return render(request, 'logisticstart/Worker/edit_worker.html', {'form': form})

def delete_worker_listing(request, id):
    worker = get_object_or_404(NewWorkerListing, id=id)
    if request.method == 'POST':
        worker.delete()
        return redirect('logisticstart-worker')
    return render(request, 'worker-delete', {'worker': worker})

# # Edit listing view 
# def edit_listing(request, pk):
#     listing = get_object_or_404(NewItemListing, pk=pk)
#     if request.method == 'POST':
#         form = CreateItemListingForm(request.POST, instance=listing)
#         if form.is_valid():
#             form.save()
#             return redirect('logisticstart-list')  # Adjust this redirect as necessary
#     else:
#         form = CreateItemListingForm(instance=listing)
#     return render(request, 'logisticstart/edit_listing.html', {'form': form})

#Dashboard
def main_dashboard(request):
    
    #Queries
    workers = NewWorkerListing.objects.all().values('id', 'worker_name', 'worker_phonenumber')
    warehouses = NewWarehouseListing.objects.all().values('warehouse_name', 'warehouse_postalcode', 'warehouse_phonenumber')
    
    dashboard = {
        'warehouses': warehouses,
        'workers': workers
    }
    return render(request, 'logisticstart/Dashboard/dashboard.html', dashboard)

#Adding of Delivery Schedule
def add_delivery_schedule(request):
    if request.method == 'POST':
        form = CreateDeliveryScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('logisticstart-delivery_schedule')  #Redirect to the same page after successful form submission
    else:
        form = CreateDeliveryScheduleForm()
    return render(request, 'logisticstart/Deliveryschedule/add_deliveryschedule.html', {'form': form})

#Displaying of Delivery Schedule
def delivery_schedule(request):
    schedules = NewDeliverySchedule.objects.all()
    return render(request, 'logisticstart/Deliveryschedule/deliveryschedule.html', {'schedules': schedules})

#Editing of Delivery Schedule
def edit_delivery_item(request, deliveryid):
    delivery_schedule = get_object_or_404(NewDeliverySchedule, pk=deliveryid)
    if request.method == 'POST':
        form = CreateDeliveryScheduleForm(request.POST, instance=delivery_schedule)
        if form.is_valid():
            form.save()
            return redirect('logisticstart-delivery_schedule')
    else:
        form = CreateDeliveryScheduleForm(instance=delivery_schedule)
    
    return render(request, 'logisticstart/Deliveryschedule/edit_delivery_schedule.html', {'form': form})

def custom_page_not_found_view(request, exception):
    return render(request, "errors/404.html", {})

def custom_error_view(request, exception=None):
    return render(request, "errors/500.html", {})

def custom_permission_denied_view(request, exception=None):
    return render(request, "errors/403.html", {})

def custom_bad_request_view(request, exception=None):
    return render(request, "errors/400.html", {})


def logisticlogin(request):
    return render(request, 'logisticstart/Login/login.html') #return logisticstart/templates/logisticstart/logisticstart.html
# views.py

def logisticregister(request):
    if request.method == 'POST':
        form = register(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully.')
            return redirect('login/')  # Redirect to a login page or another page
    else:
        form = register()

    return render(request, 'logisticstart/Login/register.html', {'form': form})
