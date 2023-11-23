from django.urls import path
from .views import *

urlpatterns = [
    path('user_n/', UserCreateNotifications.as_view()),
    path('u_n_read/', UserMarkingAsReadNotificationList.as_view()),
    path('u_a_n_read/', UserMarkingAsReadNotificationDetail.as_view()),
    path('admin_n/', AdminNotificationList.as_view()),
    path('a_n_read/', AdminMarkingAsReadNotificationList.as_view()),
    path('a_n_a_read/', AdminMarkingAsReadNotificationDetail.as_view())
]