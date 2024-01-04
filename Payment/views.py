# payme + click alohida

# import requests
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from drf_yasg.utils import swagger_auto_schema
# from .models import *
# from .serializer import *
# from User.models import *
# from User.serializer import *
#
#
# class PaymentView(APIView):
#
#     @swagger_auto_schema(request_body=PaymentSRL)
#     def post(self, request, id):
#         order = Order.objects.filter(id = id).first()
#         if order.exists():
#             id = order.user
#             user = User.objects.filter(id=id)
#             card = user.card_number
#             cvv = user.card
#             if order.payment == 'naqt':
#                 id = order.product
#                 cost = Product.object.filter(id = id).first().cost
#                 payment = int(order.quantity)*int(cost)
#             else:
#                 id = order.product
#                 cost = Product.object.filter(id=id).first().cost
#                 protsent = Product.object.filter(id=id).first().protsent
#                 payment = (int(order.quantity) * int(cost)*(1+int(protsent)/100))/int(order.oy_cre)
#             params = {
#                 'type':"to'lov",
#                 'user':str(user.name),
#                 'card':str(card),
#                 'payment':payment
#             }
#             response = requests.post(api_url=api_url, header=header, params=params)
#             if response.status_code == 200:
#                 pass
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # from User.models import *
# # #BU YOQDA PAYMENTGA JO'NATILADIGAN ZAPROSLA BILAN ISHLAYMAN
# # # Create your views here.
# # class NarxView(APIView): # payment nartni ulash joyi
# #
# #     def get(self, request, pk):
# #         user = User.objects.filter(id = pk).first()
# #         if user:
# #             order = Order.objects.filter(user = user.id).all()
# #             cost = 0
# #             if order:
# #                 for i in order:
# #                     j = Product.objects.filter(name = i.product).first()
# #                     cost += j.cost
# #                     # print(f"{i} ------- {j} ni {j.cost}")
# #                 # print(order, cost)
# #                 return Response({"status":"Malades", "cost":str(cost)})
# #             else:
# #                 return Response("Sizda hali buyurtmalar yoq")
# #         else:
# #             return Response("Bunday user yoq")
# #
# #
# #
# # class CreditPayment(APIView):  # TETS paymentni ulash joyi
# #
# #     def get(self,request, pk):
# #         user = User.objects.filter(id = pk).first()
# #         order = Order.objects.filter(user = user.id).all()
# #         cost = 0
# #         for i in order:
# #             if i.payment == "credit":
# #                 j = Product.objects.filter(name = i.product).first()
# #                 if j:
# #                     cost = (j.cost * (1+j.prosent *0.01))/ int(i.oy_cre)
# #                     pass # narxini o'zi bn dict qilib berish kk
# #             pass
# #         return Response("Malades")