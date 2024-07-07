from django import forms 
from .models import NewItemListing, NewWarehouseListing, NewWorkerListing, NewDeliverySchedule,Accounts
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password



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
    
    #To display the relevant id and name in dropbox
    def __init__(self, *args, **kwargs):
        super(CreateDeliveryScheduleForm, self).__init__(*args, **kwargs)
        self.fields['workerid'].label_from_instance = lambda obj: f"{obj.id} - {obj.worker_name}"
        self.fields['warehouseid'].label_from_instance = lambda obj: f"{obj.id} - {obj.warehouse_name}"
        self.fields['itemid'].label_from_instance = lambda obj: f"{obj.id} - {obj.item_name}"

    workerid = forms.ModelChoiceField(queryset=NewWorkerListing.objects.all(), empty_label=None, label='Worker')
    warehouseid = forms.ModelChoiceField(queryset=NewWarehouseListing.objects.filter(warehouse_status='Available'), empty_label=None, label='Warehouse')
    itemid = forms.ModelChoiceField(queryset=NewItemListing.objects.all(), empty_label=None, label='Item')
    
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
        
    #To store only the ID
    def clean_workerid(self):
        return int(self.cleaned_data['workerid'].id)
    def clean_warehouseid(self):
        return int(self.cleaned_data['warehouseid'].id)
    def clean_itemid(self):
        return int(self.cleaned_data['itemid'].id)
        


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
            print("AT leatst its checking")
        
        # Hash the password
        cleaned_data["password"] = make_password(password)

        return cleaned_data
    
class Login(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
