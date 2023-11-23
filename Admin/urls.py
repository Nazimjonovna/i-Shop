from django.urls import path
from .views import *

urlpatterns = [
    path('admin_login/', LoginView.as_view()), # admin login
    path('Begzod/', BossView.as_view()), # faqat Begzod aka uchun
    path('count/', ProductView.as_view()), # jami procustlar soni
    path('chek/<int:pk>/', AdminChekView.as_view()), # adminla qancha product qo'shganini ko'rish
    path('orders/', OrderBossView.as_view()), # Begzod aka uchun orderla istoriyasi
    path('nayuta/', NayutaView.as_view()), # Nayuta admin
    path('nayuta_check/<int:pk>/', NayutaCheckView.as_view()), # creditni tasdiqlash
    path('edit-order/', OrderEditView.as_view()), #order holatini o'zgartirish
    path('getorder/', GetOrdersView.as_view()), # get order for admin
    path('get-edit/', GetForEditOrderView.as_view()), # get  all order for edit state
    path('get-edit/<int:pk>/', GetOneOrderEditView.as_view()), # get one order for edit state and edit
    path('get_quantity/<str:name>/', GetOrderQuantityView.as_view()), # get quantity of product for admin boss
    path('delete_rec/<int:pk>/', DeleteReclamaView.as_view()), # delete reclama
    path('edit_reclama/<int:pk>/', EditReclamaView.as_view()), # edit reclama
    path('one_reclama/<int:pk>/', GetOneReclamaView.as_view()), # one reclama
    path('get_reclama/', GetReclamaView.as_view()), # get all reclama
    path('post_rec/', PostReclamaView.as_view()), # add reclama
]