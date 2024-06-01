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
    warehouse_postalcode = models.CharField(max_length=20)  # Use CharField for postal codes
    warehouse_phonenumber = models.CharField(max_length=15)  # Use CharField for phone numbers
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
