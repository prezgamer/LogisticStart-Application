from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import NewItemListing, NewWarehouseListing, NewWorkerListing, NewDeliverySchedule

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
        widgets = {
            'delivery_status': forms.RadioSelect(choices=NewItemListing.DELIVERY_STATUS)
        }

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
        widgets = {
            'worker_gender': forms.RadioSelect(choices=NewWorkerListing.GENDER_CHOICES),
            'worker_driving_license': forms.RadioSelect(choices=NewWorkerListing.DRIVING_CLASS_TYPE)
        }

class CreateWarehouseListingForm(forms.ModelForm):
    class Meta:
        model = NewWarehouseListing
        fields = [
            'warehouse_name',
            'warehouse_postalcode',
            'warehouse_phonenumber',
            'warehouse_status',
        ]
        widgets = {
            'warehouse_status': forms.RadioSelect(choices=NewWarehouseListing.WAREHOUSE_STATUS)
        }

class CreateDeliveryScheduleForm(forms.ModelForm):
    class Meta:
        model = NewDeliverySchedule
        fields = [
            'receiver_name',
            'receiver_address',
            'receiver_number',
            'workerid',
            'warehouseid',
            'itemid',
            'delivery_status',
        ]
        widgets = {
            'delivery_status': forms.RadioSelect(choices=NewDeliverySchedule.DELIVERY_STATUS)
        }


