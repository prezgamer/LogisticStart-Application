from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import NewItemListing, NewWarehouseListing, NewWorkerListing, NewDeliverySchedule,Accounts
from django.core.validators import RegexValidator

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
            'item_picture',
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
            'worker_picture',
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
            'warehouse_picture',
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


class register(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    company_phonenumber = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'tel',
            'pattern': '[0-9]{8}',
            'title': 'Company phone number must be exactly 8 digits.'
        }),
        validators=[RegexValidator(r'^\d{8}$', 'Company phone number must be exactly 8 digits and only contain numbers.')]
    )
    class Meta:
        model = Accounts
        fields = ['username', 'password', 'company_name', 'company_address', 'company_phonenumber']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password do not match")

        return cleaned_data
