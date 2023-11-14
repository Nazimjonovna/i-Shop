from django.urls import path
from .views import *

urlpatterns = [
    path('post/', PostProView.as_view()),
    path('one/<int:pk>/', EditProView.as_view()),
    path('get/', GetProView.as_view()),
]