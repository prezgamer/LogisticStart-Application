from django.shortcuts import render,redirect 
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from .models import NewItemListing, NewWarehouseListing, NewWorkerListing,NewDeliverySchedule,Accounts, UserBilling
from .forms import CreateItemListingForm, CreateWarehouseListingForm, CreateWorkerListingForm,CreateDeliveryScheduleForm,register, Login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Subquery, OuterRef
from django.conf import settings
import paypalrestsdk
from django.contrib.auth.decorators import login_required
from .paypal_utils import paypalrestsdk
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# def logistichome(request):
#     return render(request, 'logisticstart/home.html') 

# def get_current_account(request):
#     # Implement your logic to get the current account, e.g., based on session data
#     account_id = request.session.get('account_id')
#     if account_id:
#         return Accounts.objects.get(id=account_id)

def test_camera(request):
    return render(request, 'logisticstart/Login/testcamera.html')

def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        path = default_storage.save(f'uploads/{image.name}', ContentFile(image.read()))
        return JsonResponse({'status': 'success', 'path': path})
    return JsonResponse({'status': 'failed'})

def get_current_account(request):
    account_id = request.session.get('account_id')
    if account_id:
        return get_object_or_404(Accounts, accountID=account_id)
    else:
        raise PermissionDenied("You must be logged in to view this page.")

def item_list(request):
    current_account = get_current_account(request)
    items = NewItemListing.objects.filter(account=current_account)
    return render(request, 'logisticstart/items_list.html', {'items': items})

def billing(request):
    current_account = get_current_account(request)
    costs = UserBilling.objects.filter(account=current_account)
    return render(request, 'logisticstart/UserFunctions/billing.html', {'costs': costs})

#logistic warehouse items
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
            print(form.errors)  # For debugging
    else:
        form = CreateItemListingForm()
    return render(request, 'logisticstart/WarehouseItems/warehouseitemlistform.html', {'form': form, 'warehouse': warehouse})

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

def delete_warehouse_item(request, id):
    current_account = get_current_account(request)
    listing = get_object_or_404(NewItemListing, id=id, account=current_account)
    if request.method == 'POST':
        listing.delete()
        return redirect('logisticstart-warehouseitemlist', id=listing.warehouse.id)
    return render(request, 'delete_listing', {'listing': listing})
    
# logistic warehouse list
def logisticWarehouseList(request):
    current_account = get_current_account(request)
    account = Accounts.objects.filter(account=current_account)
    warehouses = NewWarehouseListing.objects.filter(account=current_account)
    return render(request, 'logisticstart/Warehouse/warehouseList.html', {'warehouses': warehouses , 'account': account})

def warehouse_item_list(request, id):
    current_account = get_current_account(request)
    warehouse = get_object_or_404(NewWarehouseListing, id=id, account=current_account)
    items = warehouse.items.all()
    return render(request, 'logisticstart/WarehouseItems/warehouseitemlist.html', {'warehouse': warehouse, 'items': items})

# new worker page
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

# add warehouses
def add_warehouse(request):
    current_account = get_current_account(request)
    if request.method == 'POST':
        form = CreateWarehouseListingForm(request.POST)
        if form.is_valid():
            warehouse = form.save(commit=False)
            warehouse.account = current_account
            warehouse.save()
            return redirect('logisticstart-warehouselist')
    else:
        form = CreateWarehouseListingForm()
    return render(request, 'logisticstart/Warehouse/add_warehouse.html', {'form': form})

# warehouse list
def warehouse_list(request):
    current_account = get_current_account(request)
    warehouses = NewWarehouseListing.objects.filter(account=current_account)
    return render(request, 'logisticstart/Warehouse/warehouseList.html', {'warehouses': warehouses})

# worker page
def worker_page(request):
    current_account = get_current_account(request)
    workers = NewWorkerListing.objects.filter(account=current_account)
    return render(request, 'logisticstart/Worker/worker.html', {'workers': workers})

def edit_delivery_item(request, deliveryid):
    current_account = get_current_account(request)
    listing = get_object_or_404(NewDeliverySchedule, deliveryid=deliveryid, account=current_account)
    if request.method == 'POST':
        form = CreateDeliveryScheduleForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('logisticstart-delivery_schedule', deliveryid=deliveryid)
    else:
        form = CreateDeliveryScheduleForm(instance=listing)
    return render(request, 'logisticstart-edit_delivery_schedule', {'form': form})

def delete_delivery_item(request, deliveryid):
    current_account = get_current_account(request)
    listing = get_object_or_404(NewDeliverySchedule, deliveryid=deliveryid, account=current_account)
    if request.method == 'POST':
        listing.delete()
        return redirect('logisticstart-delivery_schedule')
    return render(request, 'logisticstart-delete_delivery_schedule', {'listing': listing})

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

def delete_warehouse_listing(request, id):
    current_account = get_current_account(request)
    warehouse = get_object_or_404(NewWarehouseListing, id=id, account=current_account)
    if request.method == 'POST':
        warehouse.delete()
        return redirect('logisticstart-warehouselist')
    return render(request, 'delete_warehouse_listing', {'warehouse': warehouse})

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
    
def delete_worker_listing(request, id):
    current_account = get_current_account(request)
    worker = get_object_or_404(NewWorkerListing, id=id, account=current_account)
    if request.method == 'POST':
        worker.delete()
        return redirect('logisticstart-workerlist')
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
    current_account = get_current_account(request)
    workers = NewWorkerListing.objects.filter(account=current_account).values('id', 'worker_name', 'worker_phonenumber')
    warehouses = NewWarehouseListing.objects.filter(account=current_account).values('warehouse_name', 'warehouse_postalcode', 'warehouse_phonenumber')
    
    dashboard = {
        'warehouses': warehouses,
        'workers': workers
    }
    return render(request, 'logisticstart/Dashboard/dashboard.html', dashboard)

#Adding of Delivery Schedule
def add_delivery_schedule(request):
    current_account = get_current_account(request)
    if request.method == 'POST':
        form = CreateDeliveryScheduleForm(request.POST)
        if form.is_valid():
            delivery_schedule = form.save(commit=False)
            delivery_schedule.account = current_account
            delivery_schedule.save()
            return redirect('logisticstart-delivery_schedule')
    else:
        form = CreateDeliveryScheduleForm()
    return render(request, 'logisticstart/Deliveryschedule/add_deliveryschedule.html', {'form': form})

#Displaying of Delivery Schedule
def delivery_schedule(request):
    current_account = get_current_account(request)
    schedules = NewDeliverySchedule.objects.filter(account=current_account).annotate(
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
    delivery_schedule = get_object_or_404(NewDeliverySchedule, pk=deliveryid, account=current_account)

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

#paypal page
def create_payment(request):
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
                    "price": "10.10",
                    "currency": "SGD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": "10.10",
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
        return render(request, 'logisticstart/Paypal/payment_error.html', {'error': payment.error})

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return render(request, 'logisticstart/Paypal/payment_success.html')
    else:
        return render(request, 'logisticstart/Paypal/payment_error.html', {'error': payment.error})

def payment_cancelled(request):
    return render(request, 'logisticstart/Paypal/payment_cancelled.html')

def profile(request):
    current_account = get_current_account(request)
    return render(request, 'logisticstart/Profile/profile.html')

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