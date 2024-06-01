from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import NewItemListing, NewWarehouseListing, NewWorkerListing

class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class CreateItemListingForm(forms.ModelForm):
    class Meta:
        model = NewItemListing
        fields = [
            'item_name',
            'weight',
            'delivery_date',
            'sender_name',
            'sender_phone',
            'recipient_name',
            'recipient_phone',
            'delivery_status',
        ]

class CreateWorkerListingForm(forms.ModelForm):
    class Meta:
        model = NewWorkerListing
        fields = [
            'worker_name',
            'worker_age',
            'worker_gender',
            'worker_driving_license',
            'worker_phonenumber',
            'worker_NOK',
            'worker_NOK_phonenumber',
        ]

class CreateWarehouseListingForm(forms.ModelForm):
    class Meta:
        model = NewWarehouseListing
        fields = [
            'warehouse_name',
            'warehouse_postalcode',
            'warehouse_phonenumber',
            'warehouse_status',
        ]

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'postal_code', 'phone_number', 'status']