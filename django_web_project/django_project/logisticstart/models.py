from django.db import models

class NewWarehouseListing(models.Model):
    warehouse_name = models.CharField(max_length=100)
    warehouse_postalcode = models.CharField(max_length=20)
    warehouse_phonenumber = models.CharField(max_length=15)
    warehouse_status = models.CharField(max_length=100, default='Pending')

class NewItemListing(models.Model):
    item_name = models.CharField(max_length=100)
    weight = models.CharField(max_length=100)
    delivery_date = models.DateField()
    sender_name = models.CharField(max_length=100)
    sender_phone = models.CharField(max_length=15)
    recipient_name = models.CharField(max_length=100)
    recipient_phone = models.CharField(max_length=15)
    delivery_status = models.CharField(max_length=35, default='Pending')
    warehouse = models.ForeignKey(NewWarehouseListing, related_name='items', on_delete=models.CASCADE)

# New Worker Listing Model
class NewWorkerListing(models.Model):
    GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
    )
    worker_name = models.CharField(max_length=100)
    worker_age = models.IntegerField() 
    worker_gender = models.IntegerField() 
    worker_driving_license = models.CharField(max_length=100)
    worker_phonenumber = models.IntegerField()
    worker_NOK = models.CharField(max_length=100)
    worker_NOK_phonenumber = models.IntegerField()
