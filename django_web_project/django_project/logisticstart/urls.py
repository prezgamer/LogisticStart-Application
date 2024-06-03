from django.urls import path
from . import views

handler404 = 'logisticstart.views.custom_page_not_found_view'
handler500 = 'logisticstart.views.custom_error_view'
handler403 = 'logisticstart.views.custom_permission_denied_view'
handler400 = 'logisticstart.views.custom_bad_request_view'


urlpatterns = [
    path('', views.logistichome, name='logisticstart-home'), #look for logistichome function
    path('login/', views.logisticlogin, name='logisticstart-login'), #login page
    path('signup/', views.logisticsignup, name='logisticstart-signup'), #signup page
    # path('form/', views.logisticform, name='logisticstart-form'), #look for logisticstart function
    path('items/', views.logisticitems_list, name='logisticstart-list'), #look for logisticitems_list function
    path('warehouses/<int:id>/add-item/', views.logisticWarehouseItemForm, name='logisticstart-warehouseitemform'), #look for logisticWarehouseItemForm function
    path('warehouses/add-warehouse/', views.add_warehouse, name='logisticstart-addwarehouse'),
    path('warehouses/<int:id>/items/', views.warehouse_item_list, name='logisticstart-warehouseitemlist'),
    path('warehouses/', views.warehouse_list, name='logisticstart-warehouselist'),
    path('worker/add-worker/', views.logisticNewWorker, name='logisticstart-newworker'),
    #Dashboard Path
    path('dashboard/', views.logisticdashboard, name='logisticstart-dashboard'),
    #worker Path
    path('worker/', views.workerpage, name='worker'),  
]
