from django.urls import path
from . import views

handler404 = 'logisticstart.views.custom_page_not_found_view'
handler500 = 'logisticstart.views.custom_error_view'
handler403 = 'logisticstart.views.custom_permission_denied_view'
handler400 = 'logisticstart.views.custom_bad_request_view'


urlpatterns = [
    path('', views.logistichome, name='logisticstart-home'), #look for logistichome function
    path('form/', views.logisticform, name='logisticstart-form'), #look for logisticstart function
    path('login/', views.logisticlogin, name='logisticstart-login'), #look for logisticlogin function
    path('items/', views.logisticitems_list, name='logisticstart-list'), #look for logisticitems_list function
]