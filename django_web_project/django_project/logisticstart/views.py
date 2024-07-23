from django.shortcuts import render,redirect 
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from .models import NewItemListing, NewWarehouseListing, NewWorkerListing,NewDeliverySchedule,Accounts, UserBilling
from .forms import CreateItemListingForm, CreateWarehouseListingForm, CreateWorkerListingForm,CreateDeliveryScheduleForm,register, Login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Subquery, OuterRef
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .paypal_utils import paypalrestsdk
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import base64

#work in progress
def logistichome(request):
    return render(request, 'logisticstart/home.html') 

#run testcamera.html
def test_camera(request):
    return render(request, 'logisticstart/Login/testcamera.html')

#upload image function for testcamera
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        path = default_storage.save(f'worker_pictures/{image.name}', ContentFile(image.read()))
        return JsonResponse({'status': 'success', 'path': path})
    elif request.method == 'POST' and request.POST.get('image_data'):
        image_data = request.POST['image_data'].split(",")[1]
        image = ContentFile(base64.b64decode(image_data), name='captured_image.png')
        path = default_storage.save(f'worker_pictures/{image.name}', image)
        return JsonResponse({'status': 'success', 'path': path})
    return JsonResponse({'status': 'failed'})

#receive current account by getting the account_id of the account table
def get_current_account(request):
    account_id = request.session.get('account_id')
    if account_id:
        return get_object_or_404(Accounts, accountID=account_id)
    else:
        raise PermissionDenied("You must be logged in to view this page.")

#render the billing page
def billing(request):
    current_account = get_current_account(request)
    costs = UserBilling.objects.filter(account=current_account)
    total_workers = NewWorkerListing.objects.filter(account=current_account).count()


    if total_workers > 0 and total_workers < 10:
        cost = 0
    elif total_workers >= 10 and total_workers < 50:
        cost = 10
    elif total_workers >= 50:
        cost = 100

    cost_str = f"{cost:.2f}"

    return render(request, 'logisticstart/UserFunctions/billing.html', {'cost': cost_str})

#paypal page
def create_payment(request):
    current_account = get_current_account(request)
    total_workers = NewWorkerListing.objects.filter(account=current_account).count()

    if total_workers > 0 and total_workers < 10:
        cost = 0
    elif total_workers >= 10 and total_workers < 50:
        cost = 10
    elif total_workers >= 50:
        cost = 100

    cost_str = f"{cost:.2f}"

    if cost_str == "0.00":
        return render(request, 'logisticstart/Paypal/payment_error.html', {'error': "No Payment required"})

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri('/execute-payment'),
            "cancel_url": request.build_absolute_uri('/payment-cancelled')
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "total_bill",
                    "sku": "total_bill",
                    "price": cost_str,
                    "currency": "SGD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": cost_str,
                "currency": "SGD"
            },
            "description": "This is the payment transaction description."
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = link.href
                return redirect(approval_url)
    else:
        return render(request, 'logisticstart/Paypal/payment_error.html', {'error': "Transaction error"})


#execute payment using paypal
def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return render(request, 'logisticstart/Paypal/payment_success.html')
    else:
        return render(request, 'logisticstart/Paypal/payment_error.html', {'error': payment.error})

#when payment is cancelled
def payment_cancelled(request):
    return render(request, 'logisticstart/Paypal/payment_cancelled.html')

#list down the items from the item table
def warehouse_item_list(request, id):
    current_account = get_current_account(request)
    warehouse = get_object_or_404(NewWarehouseListing, id=id, account=current_account)
    items = warehouse.items.all()
    return render(request, 'logisticstart/WarehouseItems/warehouseitemlist.html', {'warehouse': warehouse, 'items': items})

#add items to respective warehouse from forms
def add_warehouse_item(request, id):
    current_account = get_current_account(request)
    warehouse = get_object_or_404(NewWarehouseListing, id=id, account=current_account)
    if request.method == 'POST':
        form = CreateItemListingForm(request.POST, request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.warehouse = warehouse
            new_item.account = current_account
            if 'item_picture' in request.FILES:
                new_item.item_picture = request.FILES['item_picture']
            new_item.save()
            return redirect('logisticstart-warehouseitemlist', id=warehouse.id)
    else:
        form = CreateItemListingForm()
    return render(request, 'logisticstart/WarehouseItems/warehouseitemlistform.html', {'form': form, 'warehouse': warehouse})

#edit warehouse items from respective warehouses
def edit_warehouse_item(request, id):
    current_account = get_current_account(request)
    listing = get_object_or_404(NewItemListing, id=id, account=current_account)
    if request.method == 'POST':
        form = CreateItemListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('logisticstart-warehouseitemlist', id=listing.warehouse.id)
    else:
        form = CreateItemListingForm(instance=listing)
    return render(request, 'logisticstart/WarehouseItems/edit_warehouse_items.html', {'form': form})

#delete warehouse items from respective warehouses
def delete_warehouse_item(request, id):
    current_account = get_current_account(request)
    listing = get_object_or_404(NewItemListing, id=id, account=current_account)
    if request.method == 'POST':
        listing.delete()
        return redirect('logisticstart-warehouseitemlist', id=listing.warehouse.id)
    return render(request, 'delete_listing', {'listing': listing})

#add new workers to worker table
def add_new_worker(request):
    current_account = get_current_account(request)
    if request.method == 'POST':
        form = CreateWorkerListingForm(request.POST, request.FILES)
        if form.is_valid():
            worker = form.save(commit=False)
            worker.account = current_account
            worker.save()
            return redirect('logisticstart-workerlist')
    else:
        form = CreateWorkerListingForm()
    return render(request, 'logisticstart/Worker/new_worker.html', {'form': form})

#add new warehouses to warehouse table
def add_warehouse(request):
    current_account = get_current_account(request)
    if request.method == 'POST':
        form = CreateWarehouseListingForm(request.POST,request.FILES)
        if form.is_valid():
            warehouse = form.save(commit=False)
            warehouse.account = current_account
            if 'item_picture' in request.FILES:
                warehouse.item_picture = request.FILES['item_picture']
            warehouse.save()
            return redirect('logisticstart-warehouselist')
    else:
        form = CreateWarehouseListingForm()
    return render(request, 'logisticstart/Warehouse/add_warehouse.html', {'form': form})

#render the warehouse list 
def warehouse_list(request):
    current_account = get_current_account(request)
    warehouses = NewWarehouseListing.objects.filter(account=current_account)
    return render(request, 'logisticstart/Warehouse/warehouseList.html', {'warehouses': warehouses})

#render the worker list
def worker_list(request):
    current_account = get_current_account(request)
    workers = NewWorkerListing.objects.filter(account=current_account)
    return render(request, 'logisticstart/Worker/worker.html', {'workers': workers})

#edit worker listing from worker list
def edit_worker_listing(request, id):
    current_account = get_current_account(request)
    listing = get_object_or_404(NewWorkerListing, id=id, account=current_account)
    if request.method == 'POST':
        form = CreateWorkerListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('logisticstart-workerlist')
    else:
        form = CreateWorkerListingForm(instance=listing)
    return render(request, 'logisticstart/Worker/edit_worker.html', {'form': form})

#delete worker listing from worker list
def delete_worker_listing(request, id):
    current_account = get_current_account(request)
    worker = get_object_or_404(NewWorkerListing, id=id, account=current_account)
    if request.method == 'POST':
        worker.delete()
        return redirect('logisticstart-workerlist')
    return render(request, 'worker-delete', {'worker': worker})

#edit warehouse listing from warehouse list
def edit_warehouse_listing(request, id):
    current_account = get_current_account(request)
    listing = get_object_or_404(NewWarehouseListing, id=id, account=current_account)
    if request.method == 'POST':
        form = CreateWarehouseListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('logisticstart-warehouselist')
    else:
        form = CreateWarehouseListingForm(instance=listing)
    return render(request, 'logisticstart/Warehouse/edit_warehouse.html', {'form': form})

#delete warehouse listing from warehouse list
def delete_warehouse_listing(request, id):
    current_account = get_current_account(request)
    warehouse = get_object_or_404(NewWarehouseListing, id=id, account=current_account)
    if request.method == 'POST':
        warehouse.delete()
        return redirect('logisticstart-warehouselist')
    return render(request, 'delete_warehouse_listing', {'warehouse': warehouse})

#Dashboard
def main_dashboard(request):
    current_account = get_current_account(request)
    
    #display deliveries with status delivering, as well as retrieving workers name using the id stored
    delivery = NewDeliverySchedule.objects.filter(account=current_account, delivery_status='Delivering').annotate(
        worker_name=Subquery(NewWorkerListing.objects.filter(id=OuterRef('worker_id')).values('worker_name')[:1])
    ).values('deliveryid', 'receiver_name',"receiver_address", 'worker_name')
    
    workers = NewWorkerListing.objects.filter(account=current_account).values('id', 'worker_name', 'worker_phonenumber')
    warehouses = NewWarehouseListing.objects.filter(account=current_account).values('warehouse_name', 'warehouse_postalcode', 'warehouse_phonenumber')
    
    dashboard = {
        'deliveries':delivery,
        'warehouses': warehouses,
        'workers': workers
    }
    return render(request, 'logisticstart/Dashboard/dashboard.html', dashboard)

#Adding of Delivery Schedule
def add_delivery_schedule(request):
    #retrieve the current account from the request
    current_account = get_current_account(request)
    if request.method == 'POST':
        #ensures that the form can filter workers, warehouses, and items to only those belonging to the current account
        form = CreateDeliveryScheduleForm(request.POST, current_account=current_account)
        if form.is_valid():
            delivery_schedule = form.save(commit=False)
            delivery_schedule.account = current_account
            delivery_schedule.save()
            return redirect('logisticstart-delivery_schedule')
    else:
        form = CreateDeliveryScheduleForm(current_account=current_account)
    return render(request, 'logisticstart/Deliveryschedule/add_deliveryschedule.html', {'form': form})

#Displaying of Delivery Schedule
def delivery_schedule_list(request):
    current_account = get_current_account(request)
    #retrieves all NewDeliverySchedule objects associated with the current account 
    #annotates each delivery schedule with the corresponding name
    schedules = NewDeliverySchedule.objects.filter(account=current_account).annotate(
        #Filters the NewXXXXXListing objects to include only those whose id matches the XXXXXX_id in the NewDeliverySchedule object
        #[:1]: retrieves the first matching name 
        worker_name=Subquery(
            NewWorkerListing.objects.filter(id=OuterRef('worker_id')).values('worker_name')[:1]
        ),
        warehouse_name=Subquery(
            NewWarehouseListing.objects.filter(id=OuterRef('warehouse_id')).values('warehouse_name')[:1]
        ),
        item_name=Subquery(
            NewItemListing.objects.filter(id=OuterRef('item_id')).values('item_name')[:1]
        )
    ).all()
    return render(request, 'logisticstart/Deliveryschedule/deliveryschedule.html', {'schedules': schedules})

#Editing of Delivery Schedule
def edit_delivery_item(request, deliveryid):
    current_account = get_current_account(request)
    #retrieve a NewDeliverySchedule with the primary key matching deliveryid and that belongs to the current_account
    delivery_schedule = get_object_or_404(NewDeliverySchedule, pk=deliveryid, account=current_account)

    if request.method == 'POST':
        #current_account is passed to the form to ensure that only relevant items are displayed in the form's fields
        form = CreateDeliveryScheduleForm(request.POST, instance=delivery_schedule, current_account=current_account)
        if form.is_valid():
            form.save()
            return redirect('logisticstart-delivery_schedule')
    else:
        form = CreateDeliveryScheduleForm(instance=delivery_schedule, current_account=current_account)
    
    return render(request, 'logisticstart/Deliveryschedule/edit_delivery_schedule.html', {'form': form})


#delete delivery items from delivery schedules
def delete_delivery_item(request, deliveryid):
    current_account = get_current_account(request)
    listing = get_object_or_404(NewDeliverySchedule, deliveryid=deliveryid, account=current_account)
    if request.method == 'POST':
        listing.delete()
        return redirect('logisticstart-delivery_schedule')
    return render(request, 'logisticstart-delete_delivery_schedule', {'listing': listing})

def custom_page_not_found_view(request, exception):
    return render(request, "errors/404.html", {})

def custom_error_view(request, exception=None):
    return render(request, "errors/500.html", {})

def custom_permission_denied_view(request, exception=None):
    return render(request, "errors/403.html", {})

def custom_bad_request_view(request, exception=None):
    return render(request, "errors/400.html", {})


#when user registers
def register_user(request):
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

#when user login
def login_user(request):
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
                    request.session['username'] = account.username  # Added to store username in session
                    request.session['company_name'] = account.company_name  # Added to store company name in session
                    request.session['company_address'] = account.company_address
                    request.session['company_phonenumber'] = account.company_phonenumber
                    print(f"Session username set: {request.session['username']}")  # Debug statement
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

#load up profile page

def profile(request):
    current_account = get_current_account(request)
    username = request.session.get('username')
    company_name = request.session.get('company_name')
    company_address = request.session.get('company_address')
    company_phonenumber = request.session.get('company_phonenumber')

    return render(request, 'logisticstart/Profile/profile.html', {
        'username': username,
        'company_name': company_name,
        'company_address': company_address,
        'company_phonenumber': company_phonenumber
    })

# def logout(request):
#     return render(request, 'logisticstart/Login/login.html')

# def profile_view(request):
#     return render(request, 'logisticstart/Profile/profile.html')

# def edit_profile_view(request):
#     # Add your view logic here
#     return render(request, 'edit_profile.html')

# def change_password_view(request):
#     # Add your view logic here
#     return render(request, 'change_password.html')