from django.urls import path
from .views import *

urlpatterns = [
    path('phone/', PhoneView.as_view()),
    path('otp/', OtpView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('get/', UserAccView.as_view()),
    path('acc/<int:pk>/', UserDetailView.as_view()),
    path('ch_pass/<int:pk>/', ChangePasswordView.as_view()),
    path('resent', ResetPasswordView.as_view()),
    path('resent_code/', ResetPasswordVerifyCode.as_view()),
    path('resent_confirm/', ResetPasswordConfirm.as_view()),
    path('ch_phone/', ChangePhoneNumber.as_view()),
    path('ch_phone_verify/', ChangePhoneNumberVerifyCode.as_view()),
    path('ch_phone_conf/', ChangePhoneNumberConfirm.as_view()),
    path('buy/', PurchaseView.as_view()),
    path('cash/', OrderCashView.as_view()), #test qilish kk
    path('cre/', OrderPayView.as_view()), #test qilish kk
    path('korzinka/<int:pk>/', Korzinka.as_view()), # Korzinka
    path('narx/<int:pk>/', NarxView.as_view()), # narxni hisoblash
    path('cre_narx/<int:pk>/', CreditPayment.as_view()) # kredtini hisoblash narxini
]