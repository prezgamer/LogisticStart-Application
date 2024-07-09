from django.shortcuts import render,redirect 
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from .models import NewItemListing, NewWarehouseListing, NewWorkerListing,NewDeliverySchedule,Accounts, UserBilling
from .forms import CreateItemListingForm, CreateWarehouseListingForm, CreateWorkerListingForm,CreateDeliveryScheduleForm,register, Login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Subquery, OuterRef



# Create your views here.
def logistichome(request):
    return render(request, 'logisticstart/home.html') #return logisticstart/templates/logisticstart/home.html

def item_list(request):
    items = NewItemListing.objects.all()
    return render(request, 'logisticstart/items_list.html', {'items': items})

def billing(request):
    costs = UserBilling.objects.all()
    return render(request, 'logisticstart/UserFunctions/billing.html', {'costs': costs})

#logistic warehouse items
def add_warehouse_item(request, id):
    warehouse = get_object_or_404(NewWarehouseListing, id=id)
    if request.method == 'POST':
        form = CreateItemListingForm(request.POST, request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.warehouse = warehouse
            if 'item_picture' in request.FILES:
                new_item.item_picture = request.FILES['item_picture']
            new_item.save()
            return redirect('logisticstart-warehouseitemlist', id=warehouse.id)
        else:
            print(form.errors)  # For debugging
    else:
        form = CreateItemListingForm()
    return render(request, 'logisticstart/WarehouseItems/warehouseitemlistform.html', {'form': form, 'warehouse': warehouse})

def edit_warehouse_item(request, id):
    listing = get_object_or_404(NewItemListing, id=id)
    if request.method == 'POST':
        form = CreateItemListingForm(request.POST, request.FILES, instance=listing)
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
        form = CreateWorkerListingForm(request.POST, request.FILES)
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

def edit_warehouse_listing(request, id):
    listing = get_object_or_404(NewWarehouseListing, id=id)
    if request.method == 'POST':
        form = CreateWarehouseListingForm(request.POST, request.FILES, instance=listing)
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
        form = CreateWorkerListingForm(request.POST, request.FILES, instance=listing)
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
    
    #OuterRef used to reference the workerid field in NewDeliverySchedule
    #[:1] limits the result to the first record 
    schedules = NewDeliverySchedule.objects.annotate(
        worker_name=Subquery(
            NewWorkerListing.objects.filter(id=OuterRef('workerid')).values('worker_name')[:1]
        ),
        warehouse_name=Subquery(
            NewWarehouseListing.objects.filter(id=OuterRef('warehouseid')).values('warehouse_name')[:1]
        ),
        item_name=Subquery(
            NewItemListing.objects.filter(id=OuterRef('itemid')).values('item_name')[:1]
        )
    ).all()

    return render(request, 'logisticstart/Deliveryschedule/deliveryschedule.html', {'schedules': schedules})

    # schedules = NewDeliverySchedule.objects.all()
    # return render(request, 'logisticstart/Deliveryschedule/deliveryschedule.html', {'schedules': schedules})

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



def logisticregister(request):
    if request.method == 'POST':
        form = register(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully.')
            return redirect('/')  # Redirect to a login page or another page
        
        else:
            print(form.errors) #error checking on my terminal
    else:
        form = register()

    return render(request, 'logisticstart/Login/register.html', {'form': form})

def logisticlogin(request):
    companies = Accounts.objects.values_list('company_name', flat=True).distinct()

    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            company_name = form.cleaned_data.get('company_name')  # Fetch company name from form
            print(f"Attempting login with username: {username} and company: {company_name}")
            try:
                # Adjust the query to also match the company name
                account = Accounts.objects.get(username=username, company_name=company_name)
                print(f"Account found: {account}")
                if check_password(password, account.password):
                    request.session['account_id'] = account.accountID
                    messages.success(request, 'You have been logged in successfully.')
                    print("Login successful")
                    return redirect('logisticstart-dashboard')  # Redirect to home or dashboard
                else:
                    messages.error(request, 'Invalid username or password.')
                    print("Invalid password")
            except Accounts.DoesNotExist:
                messages.error(request, 'Invalid username or password or company name.')
                print("Account does not exist or company name mismatch")
    else:
        form = Login()

    context = {
        'form': form,
        'companies': companies,  # Add the companies to the context
    }
    return render(request, 'logisticstart/Login/login.html', context)
