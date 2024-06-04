from django.urls import path
from . import views

handler404 = 'logisticstart.views.custom_page_not_found_view'
handler500 = 'logisticstart.views.custom_error_view'
handler403 = 'logisticstart.views.custom_permission_denied_view'
handler400 = 'logisticstart.views.custom_bad_request_view'


urlpatterns = [
    # path('', views.logistichome, name='logisticstart-home'), #look for logistichome function
    # path('login/', views.logisticlogin, name='logisticstart-login'), #login page
    # path('signup/', views.logisticsignup, name='logisticstart-signup'), #signup page
    # path('form/', views.logisticform, name='logisticstart-form'), #look for logisticstart function
    path('items/', views.logisticitems_list, name='logisticstart-list'), #look for logisticitems_list function
    path('warehouses/<int:id>/add-item/', views.logisticWarehouseItemForm, name='logisticstart-warehouseitemform'), #look for logisticWarehouseItemForm function
    path('warehouses/add-warehouse/', views.add_warehouse, name='logisticstart-addwarehouse'),
    path('warehouses/<int:id>/items/', views.warehouse_item_list, name='logisticstart-warehouseitemlist'),
    path('warehouses/', views.warehouse_list, name='logisticstart-warehouselist'),
    path('workers/add-worker/', views.logisticNewWorker, name='logisticstart-newworker'),
    path('warehouses/<int:id>/edit-warehouse-item/', views.edit_warehouse_item, name='logisticstart-editwarehouseitem'),
    path('delete/<int:id>/', views.delete_warehouse_item, name='delete_listing'),
    path('warehouses/<int:id>/edit/', views.edit_warehouse_listing, name='logisticstart-editwarehouse'),
    path('warehouses/<int:id>/delete', views.delete_warehouse_listing, name='delete_warehouse_listing'),

    #Dashboard Path
    path('', views.logisticdashboard, name='logisticstart-dashboard'),
    path('dashboard/', views.logisticdashboard, name='logisticstart-dashboard'),
    #Adding of Delivery Schedule Path
    path('deliveryschedule/add-schedule/', views.add_deliveryschedule, name='logisticstart-add_deliveryschedule'),
    #Displaying of Delivery Schedule Path
    path('deliveryschedule/schedule/', views.delivery_schedule, name='logisticstart-delivery_schedule'),
    #worker Path
    path('workers/', views.workerpage, name='logisticstart-worker'),
    path('workers/<int:id>/edit', views.edit_worker_listing, name='worker-edit'),
    path('workers/<int:id>/delete', views.delete_worker_listing, name='worker-delete')

]
