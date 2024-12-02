from django.urls import path
from . import views

urlpatterns = [
    path('',views.validate_pin,name='validate_pin'),
    path('register',views.create_account,name='register'),
    path('bridge',views.bridge,name='bridge'),
    path('transfer/<int:pk>',views.transfer,name='transfer'),
    path('deposit/<int:pk>',views.deposit,name='deposit'),
    path('withdrawal/<int:pk>',views.withdrawal,name='withdrawal'),
    path('transfersuccess',views.transfersuccess,name='transfersuccess'),
    path('forgot_pin',views.forgot_pin,name='forgot_pin'),
    path('verify_otp/<int:pk>',views.verify_otp,name='verify_otp'),
    path('reset_pin',views.reset_pin,name='reset_pin'),
]