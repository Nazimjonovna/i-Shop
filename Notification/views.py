from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .models import *
from .serializer import *
from User.models import Order, User
from Admin.models import Admin

# Create your views here.
class UserCreateNotifications(generics.ListAPIView):
    serializer_class = UserNotificationSerializer
    queryset = NotificationAdmin.objects.filter(is_read=False)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.order == True:
            user_notifs = request.user.user_n.filter(is_read=False)
            print(user_notifs)
            serializer = self.serializer_class(user_notifs, many=True)
            return Response(serializer.data)
        else:
            return Response("You are not allowed to read")


class UserMarkingAsReadNotificationList(generics.ListAPIView):
    serializer_class = AdminNotificationsSerializer
    queryset = NotificationUser.objects.filter(is_read=False)
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['user'])
    def get(self, request):
        if request.user:
            notifications = NotificationUser.objects.filter(user=request.user.id, is_read=False)
            if len(notifications) > 0:
                notifications.update(is_read=True)
                return Response({'message': 'All message successfully read!'})
            else:
                return Response({'message': 'All message has been already read!'})
        else:
            return Response("You are not allowed to read")


class UserMarkingAsReadNotificationDetail(generics.RetrieveAPIView):
    serializer_class = AdminNotificationsSerializer
    queryset = NotificationUser.objects.filter(is_read=False)
    permission_classes = [IsAuthenticated]
    my_tags = ['user']

    @swagger_auto_schema(tags=['user'])
    def get(self, request, pk):
        try:
            if request.user:
                notif = NotificationUser.objects.get(id=pk)
                notif.is_read = True
                notif.save()
                return Response({'msg': 'This message successfully read!'})
            return Response("You are not allowed to read")
        except:
            return Response("You to read")

    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []
        return super().get_parsers()


class AdminNotificationList(generics.ListAPIView):
    serializer_class = UserNotificationSerializer
    queryset = NotificationAdmin.objects.filter(is_read=False)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user:
            user_notifs = request.user.admin_n.filter(is_read=False)
            serializer = self.serializer_class(user_notifs, many=True)
            return Response(serializer.data)
        else:
            return Response("You are not allowed to read")


class AdminMarkingAsReadNotificationList(generics.ListAPIView):
    serializer_class = UserNotificationSerializer
    queryset = NotificationAdmin.objects.filter(is_read=False)
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['admin'])
    def get(self, request):
        if request.user.is_translator == True:
            notifications = NotificationAdmin.objects.filter(user=request.user.id, is_read=False)
            if len(notifications) > 0:
                notifications.update(is_read=True)
                return Response({'message': 'All message successfully read!'})
            else:
                return Response({'message': 'All message has been already read!'})
        else:
            return Response("You are not allowed to read")


class AdminMarkingAsReadNotificationDetail(generics.RetrieveAPIView):
    serializer_class = UserNotificationSerializer
    queryset = NotificationAdmin.objects.filter(is_read=False)
    permission_classes = [IsAuthenticated]
    my_tags = ['admin']

    @swagger_auto_schema(tags=['admin'])
    def get(self, request, pk):
        try:
            if request.user.is_translator == True:
                notif = NotificationAdmin.objects.get(id=pk)
                notif.is_read=True
                notif.save()
                return Response({'msg': 'This message successfully read!'})
        except:
            return Response("You are not allowed to read")

    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []
        return super().get_parsers()










































