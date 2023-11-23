from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from .models import *
from .serializer import *
from User.models import Order
from User.serializer import OrderSerializer, NayutaCheckSerializer
from Product.models import Product
from Product.serializers import ProductSerializer


# Create your views here.
class LoginView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = Admin.objects.filter(username=username, password=password).firts()
        if user:
            serializer = AdminLoginSerializer(user, many = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response("Bunday admin yoq")


class BossView(APIView): # ERROR

    def get(self, request):
        serializer = AdminLoginSerializer(Admin, many=True)
        return Response(serializer.data)

class ProductView(APIView):

    def get(self, request):
        product = Product.objects.all()
        count = 0
        for i in product:
            count +=1
        return Response({"Productlar_soni": str(count)})



class AdminChekView(APIView):

    def get(self, request, pk):
        admin = Admin.objects.filter(id=pk).first()
        if admin:
            product = Product.objects.filter(admin = pk).all()
            serializer = ProductSerializer(product, many=True)
            if product:
                return Response({"Admin":admin.username,
                                 "data":serializer.data})
            else:
                return Response("Ushbu admin hali project qo'shmadi")
        else:
            return Response("Bunday admin mavjud emas")


class OrderBossView(APIView):

    def get(self, request):
        order = Order.objects.all()
        count_n =  0
        count_c = 0
        for i in order:
            if i.payment == "naqt":
                count_n += 1
            else:
                count_c += 1
        serializer = OrderSerializer(order, many=True)
        return Response({
            "orders":serializer.data,
            "naqt": str(count_n),
            'credit': str(count_c)
        })


class NayutaView(APIView):

    def get(self, request):
        order = Order.objects.all()
        if order:
            order_n = []
            order_h = []
            or_new = 0
            or_have = 0
            sate = ['buyurtma_tayyorlanmoqda', 'yetkazib_berish_jarayoni', 'yetkazilgan']

            serializer_n = None
            serializer_h = None

            for i in order:
                if i.state == "buyurtma_berish" and i.tasdiq == False:
                    or_new += 1
                    order_n.append(i)
                elif i.state in sate and i.tasdiq == False or i.tasdiq == True:
                    or_have += 1
                    order_h.append(i)
                else:
                    continue

            if order_n:
                serializer_n = OrderSerializer(order_n, many=True)

            if order_h:
                serializer_h = OrderSerializer(order_h, many=True)

            if serializer_h:
                if serializer_n:
                    return Response({
                        "New_orders": str(or_new),
                        'News': serializer_n.data,
                        "Have_orders": str(or_have),
                        'Haves': serializer_h.data
                    })
                else:
                    return Response({
                        "New_orders": str(or_new),
                        'News': 'Yo hali',
                        "Have_orders": str(or_have),
                        'Haves': serializer_h.data
                    })
            else:
                if serializer_n:
                    return Response({
                        "New_orders": str(or_new),
                        'News': serializer_n.data,
                        "Have_orders": str(or_have),
                        'Haves': 'Yo hali'
                    })
                else:
                    return Response({
                        "New_orders": str(or_new),
                        'News': 'Yo hali',
                        "Have_orders": str(or_have),
                        'Haves': 'Yo hali'
                    })
        else:
            return Response("Bizda hali orderla mavjud emas")


class NayutaCheckView(APIView):

    @swagger_auto_schema(request_body=NayutaCheckSerializer)
    def put(self, request, pk):
        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            raise Response("Order does not exist")

        if order.state == "buyurtma_berish":
            serializer = NayutaCheckSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                order.tasdiq = request.data.get('tasdiq')
                order.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)

class GetOrdersView(APIView):

    def get(self, request):
        serializer = OrderSerializer(Order.objects.all(), many=True)
        return Response(serializer.data)



class OrderEditView(APIView):

    @swagger_auto_schema(request_body=EditorderSerializer)
    def patch(self, request, pk):
        try:
            order = Order.objects.get(id=pk)
            serializer = self.serializer_class(instance=order, data=request.data)

            if serializer.is_valid():
                serializer.save()
            return Response({'data': serializer.data, })

        except Exception as error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)


class GetForEditOrderView(APIView):

    def get(self, request):
        order = Order.objects.all()
        order_a = []
        for i in order:
            if i.state == "buyurtma_berish":
                order_a.append(i)
        serializers = OrderSerializer(order_a, many=True)
        return Response(serializers.data)

class GetOneOrderEditView(APIView):

    def get(self, request, pk):
        order = Order.objects.filter(id = pk).first()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=EditorderSerializer)
    def patch(self, request, pk):
        order = Order.objects.filter(id = pk).first()
        if order:
            order.pro_x = request.data.get('pro_x')
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response("Bunday order yo")



class GetOrderQuantityView(APIView):

    def get(self, request, name):
        product = Product.objects.filter(name = name).first()
        if product:
            quantity = product.quantity
            serializer = ProductSerializer(product, many = True)
            return Response({
                "product":serializer.data,
                "quantity":str(quantity)
            })

class PostReclamaView(APIView):

    def post(self, request):
        serializers = ProductSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)


class GetReclamaView(APIView):

    def get(self, request):
        reclama = Reclama.objects.all()
        abs = []
        if reclama:
            for i in reclama:
                if i.datetime < i.time:
                    abs.append(i)
                    serializer = ProductSerializer(abs, many=True)
                    return Response(serializer.data)
                else:
                    i.delete()
                    continue
        else:
            return Response('hozircha reclama yo')


class GetOneReclamaView(APIView):

    def get(self, request, pk):
        reclama = Reclama.objects.filter(id= pk).first()
        if reclama:
            if reclama.datetime < reclama.time:
                serializers = ProductSerializer(reclama, many=True)
                return Response(serializers.data)
            else:
                reclama.delete()
                return Response("Bu reklama muddatidan o'tgan")
        else:
            return Response("Bunday reclama yoq")


class EditReclamaView(APIView):

    def patch(self, request, pk):
        reclama = Reclama.objects.filter(id=pk).first()
        if reclama:
            reclama.file = request.data.get('file')
            serializer = ReclamaSerializer(reclama, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response("Bunday order yo")


class DeleteReclamaView(APIView):

    def delete(self, request, pk):
        reclama = Reclama.objects.filter(id = pk).first()
        reclama.delete()
        return Response("Malades o'chdi")





















