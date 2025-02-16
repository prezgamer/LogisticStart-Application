from django.shortcuts import render,redirect 
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
from .decorators import login_required


#Load the home.html 
def logistichome(request):
    return render(request, 'logisticstart/home.html') 

#run testcamera.html
def test_camera(request):
    return render(request, 'logisticstart/Login/testcamera.html')

#upload image function for testcamera
def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        uploaded_file = request.FILES['image']
        file_path = default_storage.save(f'captured_worker_pictures/{uploaded_file.name}', uploaded_file)
        return JsonResponse({'status': 'success', 'path': default_storage.url(file_path)})
    return JsonResponse({'status': 'failure', 'message': 'No image uploaded'})

#receive current account by getting the account_id of the account table
def get_current_account(request):
    account_id = request.session.get('account_id')
    if account_id:
        return get_object_or_404(Accounts, accountID=account_id)
    else:
        raise PermissionDenied("You must be logged in to view this page.")

#render the billing page
@login_required
def billing(request):
    current_account = get_current_account(request)
    account_info = current_account
    costs = UserBilling.objects.filter(account=current_account)
    total_workers = NewWorkerListing.objects.filter(account=current_account).count()


    if total_workers > 0 and total_workers < 5:
        cost = 0
    elif total_workers >= 5 and total_workers < 50:
        cost = 10
    elif total_workers >= 50:
        cost = 100
    else:
        cost = 0

    cost_str = f"{cost:.2f}"
    context = {
        'cost': cost_str,
        'account_info':account_info
    }
    return render(request, 'logisticstart/UserFunctions/billing.html', context)

#paypal page
@login_required
def create_payment(request):
    current_account = get_current_account(request)
    total_workers = NewWorkerListing.objects.filter(account=current_account).count()
    print("Number of workers: ",total_workers)

    if total_workers > 0 and total_workers < 5:
        cost = 0
    elif total_workers >= 5 and total_workers < 50:
        cost = 10
    elif total_workers >= 50:
        cost = 100
    else:
        cost = 0
    
    print("Cost: ",cost)

    if cost == 0:
        return render(request, 'logisticstart/Paypal/payment_error.html', {'error': "No Payment required"})
    else:
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
@login_required
def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return render(request, 'logisticstart/Paypal/payment_success.html')
    else:
        return render(request, 'logisticstart/Paypal/payment_error.html', {'error': payment.error})

#when payment is cancelled
@login_required
def payment_cancelled(request):
    return render(request, 'logisticstart/Paypal/payment_cancelled.html')

#list down the items from the item table
@login_required
def warehouse_item_list(request, id):
    current_account = get_current_account(request)
    account_info = current_account
    warehouse = get_object_or_404(NewWarehouseListing, id=id, account=current_account)
    items = warehouse.items.all()
    context = {
        'warehouse': warehouse,
        'account_info': account_info,
        'items' : items
    }
    return render(request, 'logisticstart/WarehouseItems/warehouseitemlist.html', context)

#add items to respective warehouse from forms
@login_required
def add_warehouse_item(request, id):
    current_account = get_current_account(request)
    account_info = current_account
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
    context={
        'form': form, 
        'warehouse': warehouse,
        'account_info' : account_info
    }
    return render(request, 'logisticstart/WarehouseItems/warehouseitemlistform.html', context)

#render edit warehouse form
@login_required
def edit_warehouse_item(request, id):
    current_account = get_current_account(request)
    account_info = current_account
    listing = get_object_or_404(NewItemListing, id=id, account=current_account)
    if request.method == 'POST':
        form = CreateItemListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('logisticstart-warehouseitemlist', id=listing.warehouse.id)
    else:
        form = CreateItemListingForm(instance=listing)
    
    context = {
        'form': form,
        'account_info': account_info,
        'warehouse_id': listing.warehouse.id
    }
    return render(request, 'logisticstart/WarehouseItems/edit_warehouse_items.html', context)


#delete warehouse items from respective warehouses
@login_required
def delete_warehouse_item(request, id):
    current_account = get_current_account(request)
    listing = get_object_or_404(NewItemListing, id=id, account=current_account)
    if request.method == 'POST':
        listing.delete()
        return redirect('logisticstart-warehouseitemlist', id=listing.warehouse.id)
    return render(request, 'delete_listing', {'listing': listing})

#add new workers to worker table
@login_required
def add_new_worker(request):
    current_account = get_current_account(request)
    if request.method == 'POST':
        form = CreateWorkerListingForm(request.POST, request.FILES)
        if form.is_valid():
            worker = form.save(commit=False)
            worker.account = current_account

            # Check if an image is uploaded
            if 'worker_picture' in request.FILES:
                worker.worker_picture = request.FILES['worker_picture']

            worker.save()
            return redirect('logisticstart-workerlist')
    else:
        form = CreateWorkerListingForm()

    context = {
        'form': form,
        'account_info': current_account
    }
    return render(request, 'logisticstart/Worker/new_worker.html', context)

#add new warehouses to warehouse table
@login_required
def add_warehouse(request):
    current_account = get_current_account(request)
    account_info = current_account
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
    context = {
        'form' : form,
        'account_info' : account_info
    }
    return render(request, 'logisticstart/Warehouse/add_warehouse.html', context)

#render the warehouse list 
@login_required
def warehouse_list(request):
    current_account = get_current_account(request)
    warehouses = NewWarehouseListing.objects.filter(account=current_account)
    account_info = current_account  # No need to fetch again, use current_account directly

    context = {
        'warehouses': warehouses,
        'account_info': account_info,
    }

    return render(request, 'logisticstart/Warehouse/warehouseList.html', context)

#render the worker list
@login_required
def worker_list(request):
    current_account = get_current_account(request)
    workers = NewWorkerListing.objects.filter(account=current_account)
    account_info = current_account

    context = {
        'workers' : workers,
        'account_info': account_info
    }
    return render(request, 'logisticstart/Worker/worker.html', context)

#edit worker listing from worker list
@login_required
def edit_worker_listing(request, id):
    current_account = get_current_account(request)
    account_info = current_account

    listing = get_object_or_404(NewWorkerListing, id=id, account=current_account)
    if request.method == 'POST':
        form = CreateWorkerListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('logisticstart-workerlist')
    else:
        form = CreateWorkerListingForm(instance=listing)
    context={
        'form': form, 
        'account_info' : account_info
    }
    return render(request, 'logisticstart/Worker/edit_worker.html', context)

#delete worker listing from worker list
@login_required
def delete_worker_listing(request, id):
    current_account = get_current_account(request)
    worker = get_object_or_404(NewWorkerListing, id=id, account=current_account)
    if request.method == 'POST':
        worker.delete()
        return redirect('logisticstart-workerlist')
    return render(request, 'worker-delete', {'worker': worker})

#edit warehouse listing from warehouse list
@login_required
def edit_warehouse_listing(request, id):
    current_account = get_current_account(request)
    account_info = current_account

    listing = get_object_or_404(NewWarehouseListing, id=id, account=current_account)
    if request.method == 'POST':
        form = CreateWarehouseListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('logisticstart-warehouselist')
    else:
        form = CreateWarehouseListingForm(instance=listing)
    context={
        'form': form,
        'account_info' : account_info
    }
    return render(request, 'logisticstart/Warehouse/edit_warehouse.html', context)

#delete warehouse listing from warehouse list
@login_required
def delete_warehouse_listing(request, id):
    current_account = get_current_account(request)
    warehouse = get_object_or_404(NewWarehouseListing, id=id, account=current_account)
    if request.method == 'POST':
        warehouse.delete()
        return redirect('logisticstart-warehouselist')
    return render(request, 'delete_warehouse_listing', {'warehouse': warehouse})

#Dashboard
@login_required
def main_dashboard(request):
    current_account = get_current_account(request)
    
    #display deliveries with status delivering, as well as retrieving workers name using the id stored
    delivery = NewDeliverySchedule.objects.filter(account=current_account, delivery_status='Delivering').annotate(
        worker_name=Subquery(NewWorkerListing.objects.filter(id=OuterRef('worker_id')).values('worker_name')[:1])
    ).values('deliveryid', 'receiver_name',"receiver_address", 'worker_name')
    
    workers = NewWorkerListing.objects.filter(account=current_account).values('id', 'worker_name', 'worker_phonenumber')
    warehouses = NewWarehouseListing.objects.filter(account=current_account).values('warehouse_name', 'warehouse_postalcode', 'warehouse_phonenumber')
    account_info = current_account
    dashboard = {
        'deliveries':delivery,
        'warehouses': warehouses,
        'workers': workers,
        'account_info' : account_info
    }
    return render(request, 'logisticstart/Dashboard/dashboard.html', dashboard)

#Adding of Delivery Schedule
@login_required
def add_delivery_schedule(request):
    #retrieve the current account from the request
    current_account = get_current_account(request)
    account_info = current_account
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
    context = {
        'form' : form,
        'account_info' : account_info
    }
    return render(request, 'logisticstart/Deliveryschedule/add_deliveryschedule.html', context)

#Displaying of Delivery Schedule
@login_required
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
    account_info = current_account
    context = {
        'schedules' : schedules,
        'account_info' : account_info
    }
    return render(request, 'logisticstart/Deliveryschedule/deliveryschedule.html',context)

#Editing of Delivery Schedule
@login_required
def edit_delivery_item(request, deliveryid):
    current_account = get_current_account(request)
    account_info = current_account
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
    context = {
        'form':form,
        'account_info' : account_info

    }

    return render(request, 'logisticstart/Deliveryschedule/edit_delivery_schedule.html', context)


#delete delivery items from delivery schedules
@login_required
def delete_delivery_item(request, deliveryid):
    current_account = get_current_account(request)
    listing = get_object_or_404(NewDeliverySchedule, deliveryid=deliveryid, account=current_account)
    if request.method == 'POST':
        listing.delete()
        return redirect('logisticstart-delivery_schedule')
    return render(request, 'logisticstart-delete_delivery_schedule', {'listing': listing})

@login_required
def custom_page_not_found_view(request, exception):
    current_account = get_current_account(request)
    account_info = current_account
    return render(request, "errors/404.html", {'account_info':account_info})

@login_required
def custom_error_view(request, exception=None):
    current_account = get_current_account(request)
    account_info = current_account
    return render(request, "errors/404.html", {'account_info':account_info})

@login_required
def custom_permission_denied_view(request, exception=None):
    current_account = get_current_account(request)
    account_info = current_account
    return render(request, "errors/404.html", {'account_info':account_info})

@login_required
def custom_bad_request_view(request, exception=None):
    current_account = get_current_account(request)
    account_info = current_account
    return render(request, "errors/404.html", {'account_info':account_info})



#when user registers
def register_user(request):
    if request.method == 'POST':
        form = register(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully.')
            return redirect('logisticstart-login')  # Redirect to a login page or another page
        
        else:
            print(form.errors) #error checking on my terminal
    else:
        form = register()

    return render(request, 'logisticstart/Login/register.html', {'form': form})

#when user login
def login_user(request):
    companies = Accounts.objects.values_list('company_name', flat=True).distinct()
    error_message = None

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
                    error_message = 'Invalid username or password.'
                    print("Invalid password")
            except Accounts.DoesNotExist:
                messages.error(request, 'Invalid username or password or company name.')
                error_message = 'Invalid username or password or company name.'
                print("Account does not exist or company name mismatch")
    else:
        form = Login()

    context = {
        'form': form,
        'companies': companies,  # Add the companies to the context
        'error_message' : error_message
    }
    return render(request, 'logisticstart/Login/login.html', context)

#load up profile page
@login_required
def profile(request):
    try:
        current_account = get_current_account(request)
    except PermissionDenied:
        return redirect('login_url')  # Replace 'login_url' with the actual URL or URL name of your login page

    account_info = current_account  # No need to fetch again, use current_account directly
    return render(request, 'logisticstart/Profile/profile.html', {
        'account_info': account_info,
    })


def logout(request):
    if 'username' in request.session:
        del request.session['username']
        #messages.success(request, 'You have successfully logged out.')
    return redirect('logisticstart-home')