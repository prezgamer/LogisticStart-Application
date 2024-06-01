from django.contrib import admin
from .models import NewItemListing, NewWarehouseListing, NewWorkerListing

admin.site.register(NewItemListing)
admin.site.register(NewWarehouseListing)
admin.site.register(NewWorkerListing)

