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
    #Dropdown field for worker,warehouse and items
    worker = forms.ModelChoiceField(queryset=NewWorkerListing.objects.none(), empty_label=None, label='Worker')
    warehouse = forms.ModelChoiceField(queryset=NewWarehouseListing.objects.none(), empty_label=None, label='Warehouse')
    item = forms.ModelChoiceField(queryset=NewItemListing.objects.none(), empty_label=None, label='Item')

    class Meta:
        model = NewDeliverySchedule
        fields = [
            'receiver_name',
            'receiver_address',
            'receiver_number',
            'worker',
            'warehouse',
            'item',
            'delivery_status',
        ]
        widgets = {
            'delivery_status': forms.RadioSelect(choices=NewDeliverySchedule.DELIVERY_STATUS)
        }
    #initialize method 
    def __init__(self, *args, **kwargs):
        current_account = kwargs.pop('current_account', None)
        super(CreateDeliveryScheduleForm, self).__init__(*args, **kwargs)
        
        if current_account:
            #filtering to only include the fields associated with the current account.
            self.fields['worker'].queryset = NewWorkerListing.objects.filter(account=current_account)
            #will only display warehouses that has the available status
            self.fields['warehouse'].queryset = NewWarehouseListing.objects.filter(account=current_account, warehouse_status='Available') 
            self.fields['item'].queryset = NewItemListing.objects.filter(account=current_account)
        #making custom labels to include both the id and name of that specific thing
        self.fields['worker'].label_from_instance = lambda obj: f"{obj.id} - {obj.worker_name}"
        self.fields['warehouse'].label_from_instance = lambda obj: f"{obj.id} - {obj.warehouse_name}"
        self.fields['item'].label_from_instance = lambda obj: f"{obj.id} - {obj.item_name}"
        
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
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if Accounts.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with this username already exists.")
        return username
    
    def clean_company_name(self):
        company_name = self.cleaned_data.get('company_name')
        if Accounts.objects.filter(company_name=company_name).exists():
            raise forms.ValidationError("A company with this name already exists.")
        return company_name

    
class Login(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    company_name = forms.CharField(max_length=100)
