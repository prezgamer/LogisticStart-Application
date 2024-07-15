from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.contrib.auth.models import User

#login

class Accounts(models.Model):
    accountID = models.AutoField(primary_key= True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    company_address = models.CharField(max_length=255)    
    company_phonenumber = models.CharField(max_length=15)

class NewWarehouseListing(models.Model):
    WAREHOUSE_STATUS = (
        ('Pending', 'Pending'),
        ('Available', 'Available'),
        ('Unavailable', 'Unavailable'),
    )
    warehouse_name = models.CharField(max_length=100)
    warehouse_postalcode = models.IntegerField()
    warehouse_phonenumber = models.IntegerField()
    warehouse_status = models.CharField(max_length=100, default='Pending', choices=WAREHOUSE_STATUS)
    warehouse_picture=models.ImageField(upload_to='warehouse_pictures/', default='images/null.jpg')
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name='warehouses', default=1)

class NewItemListing(models.Model):
    item_picture = models.ImageField(upload_to='images/', default='images/null.jpg')
    DELIVERY_STATUS = (
        ('Pending', 'Pending'),
        ('Delivering', 'Delivering'),
        ('Delivered', 'Delivered')
    )
    item_name = models.CharField(max_length=100)
    weight = models.IntegerField()
    delivery_date = models.DateField()
    sender_name = models.CharField(max_length=100, validators=[
            RegexValidator(
                regex='^[a-zA-Z ]+$',
                message='Name must contain only letters.'
            )
        ])
    sender_phone = models.CharField(max_length=15)
    recipient_name = models.CharField(max_length=100, validators=[
            RegexValidator(
                regex='^[a-zA-Z ]+$',
                message='Name must contain only letters.'
            )
        ])
    recipient_phone = models.CharField(max_length=15)
    delivery_status = models.CharField(max_length=35, default='Pending', choices=DELIVERY_STATUS)
    warehouse = models.ForeignKey('NewWarehouseListing', related_name='items', on_delete=models.CASCADE)
    account = models.ForeignKey(Accounts, related_name='items' , on_delete=models.CASCADE)

# New Worker Listing Model
class NewWorkerListing(models.Model):
    account = models.ForeignKey(Accounts, related_name='workers', on_delete=models.CASCADE, default='1')
    worker_picture=models.ImageField(upload_to='worker_pictures/', default='images/null.jpg')
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    DRIVING_CLASS_TYPE = (
        ('Class 2', '2'),
        ('Class 2A', '2A'),
        ('Class 2B', '2B'),
        ('Class 3', '3'),
        ('Class 3A', '3A'),
        ('Class 3C', '3C'),
        ('Class 3CA', '3CA'),
        ('Class 4', '4'),
        ('Class 4A', '4A'),
        ('Class 5', '5')
    )
    worker_name = models.CharField(max_length=100, validators=[
            RegexValidator(
                regex='^[a-zA-Z ]+$',
                message='Name must contain only letters.'
            )
        ])
    worker_age = models.IntegerField(validators=[
            MinValueValidator(18),
            MaxValueValidator(90)
        ])
    worker_gender = models.CharField(max_length=1, choices=GENDER_CHOICES)  
    worker_driving_license = models.CharField(max_length=30, choices=DRIVING_CLASS_TYPE)
    worker_phonenumber = models.IntegerField()
    worker_NOK = models.CharField(max_length=100, validators=[
            RegexValidator(
                regex='^[a-zA-Z ]+$',
                message='Name must contain only letters.'
            )
        ])
    worker_NOK_phonenumber = models.IntegerField()
   
    
    
#New Delivery Schedule Listing
class NewDeliverySchedule(models.Model):
    DELIVERY_STATUS = (
        ('Pending', 'Pending'),
        ('Delivering', 'Delivering'),
        ('Delivered', 'Delivered')
    )
    
    deliveryid = models.AutoField(primary_key=True)
    receiver_name = models.CharField(max_length=255, validators=[
        RegexValidator(
            regex='^[a-zA-Z ]+$',
            message='Name must contain only letters.'
        )
    ])
    receiver_address = models.CharField(max_length=255)
    receiver_number = models.CharField(max_length=15)
    worker = models.ForeignKey(NewWorkerListing, related_name='deliveries', on_delete=models.CASCADE)
    warehouse = models.ForeignKey(NewWarehouseListing, related_name='deliveries', on_delete=models.CASCADE)
    item = models.ForeignKey(NewItemListing, related_name='deliveries', on_delete=models.CASCADE)
    account = models.ForeignKey(Accounts, related_name='deliveries' , default=1, on_delete=models.CASCADE)
    delivery_status = models.CharField(max_length=255, choices=DELIVERY_STATUS, default='Pending')

#billing
class UserBilling(models.Model):
    userCredits = models.IntegerField()
    userPrepayments = models.IntegerField()
    userTotalUsage = models.IntegerField()
    account = models.ForeignKey(Accounts, related_name='billing', on_delete=models.CASCADE, default='1')
    
