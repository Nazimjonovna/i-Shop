from django.urls import path
from .views import *

urlpatterns = [
    path('post/', PostProView.as_view()),
    path('one/<int:pk>/', EditProView.as_view()),
    path('get/', GetProView.as_view()),
    path('info', AddProductInfoView.as_view()),
    path('images', AddImageView.as_view()),
    path('products/<str:category>/', AddRecProView.as_view()),
    path('get_rec_pro/<str:category>/', GetRecProView.as_view()),
    # path('get_cre/<int:pk>/', CreditProductView.as_view()), # productni credit narxi
]