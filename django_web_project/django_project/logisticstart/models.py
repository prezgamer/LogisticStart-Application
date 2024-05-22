from django.db import models

# Create your models here.
class NewListing(models.Model):
    item_name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=100)
    delivery_date = models.DateField()
    sender_name = models.CharField(max_length=100)
    sender_phone = models.CharField(max_length=15)
    sender_email = models.EmailField()
    recipient_name = models.CharField(max_length=100)
    recipient_phone = models.CharField(max_length=15)
    recipient_email = models.EmailField()
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)

    def __str__(self):
        return self.item_name