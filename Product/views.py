from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from User.models import Order
from User.serializer import OrderSerializer

from .models import *
from .serializers import *

# Create your views here.
class PostProView(APIView):
    parser_classes = [MultiPartParser, ]

    @swagger_auto_schema(request_body = ProductSerializer)
    def post(self, request):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class AddProductInfoView(APIView):
    parser_classes = [MultiPartParser, ]
    @swagger_auto_schema(request_body = ProducInfoSerializer)
    def post(self, request):
        serializer = ProducInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

class AddImageView(APIView):
    parser_classes = [MultiPartParser, ]
    @swagger_auto_schema(request_body = ImageSerializer)
    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class AddRecProView(APIView):
    parser_classes = [MultiPartParser, ]
    @swagger_auto_schema(request_body = RecProSerializer)
    def post(self, request, category):
        pro_rec = RecPro.objects.all() 
        if pro_rec:
            for i in pro_rec:
                if ProductInfo.objects.filter(product = i.product.id).first().category == category:
                    i.delete()
                    serializers = RecProSerializer(data = request.data)
                    if serializers.is_valid():
                        serializers.save()
                        return Response(serializers.data)
                    else:
                        return Response(serializers.errors)
                else:
                    serializers = RecProSerializer(data = request.data)
                    if serializers.is_valid():
                        serializers.save()
                        return Response(serializers.data)
                    else:
                        return Response(serializers.errors)
        else:
                    serializers = RecProSerializer(data = request.data)
                    if serializers.is_valid():
                        serializers.save()
                        return Response(serializers.data)
                    else:
                        return Response(serializers.errors)
        

class GetRecProView(APIView):
    def get(self, request, category):
        pro_rec = RecPro.objects.all()
        print("mana", pro_rec)
        if pro_rec:
            als = {'producst' : []}
            for i in pro_rec:
                print("lalalalalala", i.product.id)
                n = {}
                produ = Product.objects.filter(id = i.product.id).first()
                pro_i = ProductInfo.objects.filter(product = i.product.id).first()
                info = ProducInfoSerializer(pro_i).data
                n['info'] = info
                product = ProductSerializer(produ).data
                n['product'] = product
                pro_r = RecProSerializer(i).data
                n['image'] = pro_r
            als['producst'].append(n)
            return Response(als)
        else:
            return Response("Hali bosh")
        




class EditProView(APIView):
    permission_classes = [IsAdminUser, ]
    parser_classes = [MultiPartParser, ]

    @swagger_auto_schema(request_body=ProductSerializer)
    def patch(self, request, pk):
        product = Product.objects.filter(id = pk).first()
        if product:
            data = request.data
            serializer = ProductSerializer(data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response("Bizda hozircha bunday mahsulot yo'q")

    @swagger_auto_schema(request_body=ProductSerializer)
    def delete(self, request, pk):
        product = Product.objects.filter(id=pk)
        product.delete()
        return Response('Successfuly) ')

    def get(self, request, pk):
        product = Product.objects.filter(id = pk)
        if product:
            serializer = ProductSerializer(product, many = True)
            return Response(serializer.data)
        else:
            return Response("Bizda bunday mahsulot topilmadi")

class GetProView(APIView):
    permission_classes = [AllowAny, ]
    parser_classes = [MultiPartParser, ]

    def get(self,request):
        products = Product.objects.all()
        response_data = {"products": []}

        if products.exists():
            for product in products:
                if product.tasdiq:
                    inf = ProductInfo.objects.get(product=product.id)
                    info = ProducInfoSerializer(inf).data
                    ima = Image.objects.filter(pro_id=product.id).all()
                    ims = []
                    for i in ima:
                        ims.append(i)
                    image = ImageSerializer(ims, many = True).data
                    sum_cre = (int(product.cost) * (1 + product.prosent)) / 12
                    serialized_product = ProductSerializer(product).data
                    serialized_product['credit_12ga'] = str(sum_cre)
                    serialized_product['info'] = info
                    serialized_product['image'] = str(image)
                    response_data["products"].append(serialized_product)

                    return Response(response_data)
                else:
                    return Response("Bizda hozircha mahsulotlar yo'q")
        else:
            return Response("Hozircha ma'lumot topilmadi")



class CreditProductView(APIView): # Malades)

    def get(self, request, pk):
        product = Product.objects.filter(id = pk).first()
        if product:
            cost = (product.cost *(1+0.01*int(product.prosent)))/12
            serializers = ProductSerializer(product)
            return Response({
                "cost_credit":str(cost),
                "data":serializers.data
            })
        else:
            return Response("Bunday mahsulot yoq")






