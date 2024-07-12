from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


handler404 = 'logisticstart.views.custom_page_not_found_view'
handler500 = 'logisticstart.views.custom_error_view'
handler403 = 'logisticstart.views.custom_permission_denied_view'
handler400 = 'logisticstart.views.custom_bad_request_view'


urlpatterns = [
    # path('', views.logistichome, name='logisticstart-home'), #look for logistichome function
    # path('login/', views.logisticlogin, name='logisticstart-login'), #login page
    # path('signup/', views.logisticsignup, name='logisticstart-signup'), #signup page
    # path('form/', views.logisticform, name='logisticstart-form'), #look for logisticstart function
    # path('items/', views.item_list, name='logisticstart-list'), #look for logisticitems_list function

    #Warehouse Item paths
    path('warehouses/<int:id>/add-item/', views.add_warehouse_item, name='logisticstart-warehouseitemform'), #look for logisticWarehouseItemForm function
    path('warehouses/<int:id>/items/', views.warehouse_item_list, name='logisticstart-warehouseitemlist'),
    path('warehouses/<int:id>/edit-warehouse-item/', views.edit_warehouse_item, name='logisticstart-editwarehouseitem'),
    path('warehouses/<int:id>/delete-items/', views.delete_warehouse_item, name='delete_listing'),

    #Warehouse paths
    path('warehouses/', views.warehouse_list, name='logisticstart-warehouselist'),
    path('warehouses/add-warehouse/', views.add_warehouse, name='logisticstart-addwarehouse'),
    path('warehouses/<int:id>/edit/', views.edit_warehouse_listing, name='logisticstart-editwarehouse'),
    path('warehouses/<int:id>/delete', views.delete_warehouse_listing, name='delete_warehouse_listing'),

    #Dashboard Path
    path('dashboard/', views.main_dashboard, name='logisticstart-dashboard'),

    #Delivery Schedule Paths
    path('deliveryschedule/add-schedule/', views.add_delivery_schedule, name='logisticstart-add_deliveryschedule'),
    path('deliveryschedule/', views.delivery_schedule, name='logisticstart-delivery_schedule'),
    path('deliveryschedule/<int:deliveryid>/edit/', views.edit_delivery_item, name='logisticstart-edit_delivery_schedule'),
    path('deliveryschedule/<int:deliveryid>/delete', views.delete_delivery_item, name='logisticstart-delete_delivery_schedule'),

    #Worker Paths
    path('workers/', views.worker_page, name='logisticstart-worker'),
    path('workers/<int:id>/edit', views.edit_worker_listing, name='worker-edit'),
    path('workers/<int:id>/delete', views.delete_worker_listing, name='worker-delete'),
    path('workers/add-worker/', views.add_new_worker, name='logisticstart-newworker'),

    #User Functions Paths
    path('billing/', views.billing, name='logisticstart-billing'),

    #login
    path('', views.logisticlogin, name='logisticstart-login'),
    path('register/', views.logisticregister, name='logisticstart-register'),

    #Paypal
    path('create-payment/', views.create_payment, name='create_payment'),
    path('execute-payment/', views.execute_payment, name='execute_payment'),
    path('payment-cancelled/', views.payment_cancelled, name='payment_cancelled'),

    #Profile Paths
    path('profile/', views.profile_view, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/change-password/', views.change_password_view, name='change_password'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)