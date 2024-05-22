from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import NewListing

class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class CreateListingForm(forms.ModelForm):
    class Meta:
        model = NewListing
        fields = [
            'item_name',
            'item_type',
            'delivery_date',
            'sender_name',
            'sender_phone',
            'sender_email',
            'recipient_name',
            'recipient_phone',
            'recipient_email',
            'customer_name',
            'customer_email',
            'customer_phone'
        ]
