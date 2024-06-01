from django.db import models

# New Item Listing Model
class NewItemListing(models.Model):
    item_name = models.CharField(max_length=100)
    weight = models.CharField(max_length=100)
    delivery_date = models.DateField()
    sender_name = models.CharField(max_length=100)
    sender_phone = models.CharField(max_length=15)
    recipient_name = models.CharField(max_length=100)
    recipient_phone = models.CharField(max_length=15)
    delivery_status = models.CharField(max_length=35, default='Pending')

# New Warehouse Listing Model
class NewWarehouseListing(models.Model):
    warehouse_name = models.CharField(max_length=100)
    warehouse_postalcode = models.IntegerField() #help me check if the field is correct
    warehouse_phonenumber = models.IntegerField() #help me check if the field is correct
    warehouse_status = models.CharField(max_length=100, default='Pending') 

    def __str__(self):
        return self.warehouse_name

# New Worker Listing Model
class NewWorkerListing(models.Model):
    worker_name = models.CharField(max_length=100)
    worker_age = models.IntegerField() 
    worker_gender = models.IntegerField() 
    worker_driving_license = models.CharField(max_length=100)
    worker_phonenumber = models.IntegerField()
    worker_NOK = models.CharField(max_length=100)
    worker_NOK_phonenumber = models.IntegerField()

class Warehouse(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    name = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.name