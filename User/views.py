import requests
import pytz
import datetime as d
from random import randint
from rest_framework import generics
from django.conf import settings
from get_sms import Getsms
from drf_yasg.utils import swagger_auto_schema
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, parsers
from Product.serializers import *
from Product.models import *
from .serializer import *
from .models import *

utc = pytz.timezone(settings.TIME_ZONE)
min = 1

# Create your views here.
def send_sms(phone_number, step_reset=None, change_phone=None):
    try:
        verify_code = randint(1111, 9999)
        try:
            obj = Verification.objects.get(phone=phone_number)
        except Verification.DoesNotExist:
            obj = Verification(phone=phone_number, verify_code=verify_code)
            obj.step_reset = step_reset
            obj.step_change_phone = change_phone
            obj.save()
            context = {'phone_number': str(obj.phone), 'verify_code': obj.verify_code,
                       'lifetime': _(f"{min} minutes")}
            return context
        time_now = d.datetime.now(utc)
        diff = time_now - obj.created
        three_minute = d.timedelta(minutes=min)
        if diff <= three_minute:
            time_left = str(three_minute - diff)
            return {'message': _(f"Try again in {time_left[3:4]} minute {time_left[5:7]} seconds")}
        obj.delete()
        obj = Verification(phone=phone_number)
        obj.verify_code = verify_code
        obj.step_reset = step_reset
        obj.step_change_phone = change_phone
        obj.save()
        context = {'phone_number': str(obj.phone), 'verify_code': obj.verify_code, 'lifetime': _(f"{min} minutes")}
        return context
    except Exception as e:
        print(f"\n[ERROR] error in send_sms <<<{e}>>>\n")

# requests.post("http://sms-service.m1.uz/send_sms/", {"phone_number": 998901361752, "text": "Hello"})


class SendSms(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SendSmsSerializer
    parser_classes = [parsers.MultiPartParser]

    def post(self, request):
        serializer = SendSmsSerializer(data=request.data)
        if serializer.is_valid():
            login = "Name_of_work"
            password = "B180Ns49DnRbuPX9686R"
            nickname = "ShopUz"

            message = Getsms(login=login, password=password, nickname=nickname)
            phone_numbers = [serializer.data['phone_number']]

            results = message.send_message(phone_numbers=phone_numbers, text=serializer.data['text'])

            if 'error' in results:
                print(results)

            for result in results:
                print(result)
            return Response({"msg": f"Send SMS successfully to {serializer.data['phone_number']}"})
        else:
            return Response({"msg": serializer.errors})


class PhoneView(APIView):
    arser_classes = [parsers.MultiPartParser]

    @swagger_auto_schema(request_body=PhoneSRL, tags=['Phone'])
    def post(self, request):
        phone_number = request.data.get("phone")
        if phone_number.isdigit() and len(phone_number) > 8:
            user = User.objects.filter(phone__iexact=phone_number)
            if user.exists():
                return Response({
                    "status": False,
                    "detail": "Bu raqam avval registerdan otgan."
                })
            else:
                otp = send_sms(phone_number)
                if 'verify_code' in otp:
                    code = str(otp['verify_code'])
                    try:
                        validate = ValidatedOtp.objects.get(phone=phone_number)
                        if validate.validated:
                            validate.otp = code
                            validate.validated = False
                            validate.save()

                    except ValidatedOtp.DoesNotExist as e:
                        phon = ValidatedOtp.objects.filter(phone__iexact=phone_number)
                        if not phon.exists():
                            ValidatedOtp.objects.create(phone=phone_number, otp=code, validated=False)
                        else:
                            Response({"phone": "mavjud"})

                return Response({
                    "status": True,
                    "detail": "SMS xabarnoma jo'natildi",
                    "code": otp  # <--vaqtinchalik qo'shildi
                })
        else:
            if len(phone_number) < 8:
                return Response({"detail": "Telefon raqamingizni kod bilan kiriting!"})
            else:
                return Response({
                    "status": False,
                    "detail": "Telefon raqamni kiriting ."
                })

    def send_otp(phone, otp):
        if phone:
            otp = randint(1111, 9999)
            print(otp)
            return otp
        else:
            return False


class OtpView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [parsers.MultiPartParser]

    @swagger_auto_schema(request_body=OtpSRL, tags=['Register'])
    def post(self, request):
        phone_number = request.data.get('phone', True)
        code_send = request.data.get('otp', True)
        if not phone_number and code_send:
            return Response({
                'status': False,
                'detail': 'Otpni va phone ni kiriting'
            })

        try:
            verify = ValidatedOtp.objects.get(phone=phone_number, validated=False)
            if verify.otp == code_send:
                verify.count += 1
                verify.validated = True
                verify.save()

                return Response({
                    'status': True,
                    'detail': "Otp to'g'ri"
                })
            else:
                return Response({
                    'status': False,
                    'error': "Otpni to'g'ri kiriting"})

        except ValidatedOtp.DoesNotExist as e:
            return Response({
                'error': "Otp aktiv emas yoki mavjud emas, boshqa otp oling"
            })



class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_classes = RegisterSRL
    parser_classes = [parsers.MultiPartParser]

    @swagger_auto_schema(request_body=RegisterSRL, tags=['Register'])
    def post(self, request):
        request.POST._mutable = True
        password = request.data['password'][:]
        request.data['password'] = make_password(password)
        serializer = True
        request.POST._mutable = True

        try:
            verify = ValidatedOtp.objects.filter(phone__iexact=request.data['phone'], validated=True)
            if verify.exists():
                if serializer:
                    user_obj = User(phone=request.data['phone'])
                    user_obj.password = request.data['password']
                    user_obj.name = request.data['name']
                    user_obj.save()
                    access_token = AccessToken().for_user(user_obj)
                    refresh_token = RefreshToken().for_user(user_obj)
                    return Response({
                        "access": str(access_token),
                        "refresh": str(refresh_token),
                        "phone": str(user_obj.phone),
                        "name": str(user_obj.name),
                        "password": str(user_obj.password)
                    })

        except:
            return Response({
                "status": False,
                "detail": "Siz bir martalik mahfiy kodni kiritmgansiz. Shuning uchun ro'yhatdan o'ta olmaysiz!"
            })


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = Log
    parser_classes = [parsers.MultiPartParser]

    @swagger_auto_schema(request_body=Log)
    def post(self, request):
        try:
            print("try")
            user = User.objects.get(phone=request.data['phone'])

            if check_password(request.data['password'], user.password):
                print('if')
                phone = User.objects.get(phone=request.data['phone'])
                access_token = AccessToken().for_user(phone)
                refresh_token = RefreshToken().for_user(phone)
                return Response({
                    "id": phone.id,
                    "access": str(access_token),
                    "refresh": str(refresh_token),
                })
            else:
                print('else')
                return Response({'Xato': "Noto'g'ri password kiritdingiz :("})

        except:
            print('except')
            return Response({'Xato': 'Bunday user mavjud emas :('})


class UserAccView(APIView):
    parser_classes = [parsers.MultiPartParser]

    def get(self, request, *args, **kwargs):
        serializer=GetUserInfoSerializer(User.objects.all(), many=True)
        return Response(serializer.data)




class UserDetailView(APIView):

    permission_classes = [IsAuthenticated,]
    serializer_class = Accaunt
    queryset = User.objects.all()
    parser_classes = [parsers.MultiPartParser]

    @swagger_auto_schema(tags=['Account'])
    def get(self, request, pk):

        try:
            user = User.objects.get(id=pk)
            print("try", user)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = GetUserInfoSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(request_body=Accaunt, tags=['Account'])
    def patch(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            serializer = self.serializer_class(instance=user, data=request.data)

            if serializer.is_valid():
                serializer.save()
            return Response({'data': serializer.data, })

        except Exception as error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(tags=['Account'])
    def delete(self, request, pk):
        user = User.objects.get(id=pk)

        if user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    parser_classes = [parsers.MultiPartParser]
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    my_tags = ['Change-Password']

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(instance=self.request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Password successfully updated'}, status=status.HTTP_200_OK)


class VerifyCodeView(APIView): # tel o'zgartirilgandagi verificatsiya
    serializer_class = VerifyCodeSerializer
    permission_classes = [AllowAny]
    parser_classes = [parsers.MultiPartParser]
    queryset = Verification.objects.all()

    @swagger_auto_schema(request_body=VerifyCodeSerializer, tags=['Password-Reset'])
    def put(self, request, *args, **kwargs):
        data = request.data
        try:
            obj = Verification.objects.get(phone=data['phone'])
            serializer = VerifyCodeSerializer(instance=obj, data=data)
            if serializer.is_valid():
                serializer.save()
                if serializer.data['step_change_phone'] == 'confirmed':
                    user = request.user
                    user.phone = data['phone']
                    user.save()
                    return Response({'message': 'Your phone number has been successfully changed!'},
                                status=status.HTTP_202_ACCEPTED)
                return Response({'message': 'This phone number has been successfully verified!'},
                                status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Verification.DoesNotExist:
            return Response({'error': 'Phone number or verify code incorrect!'}, statusis_pupil=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PhoneSRL
    parser_classes = [parsers.MultiPartParser]
    my_tags = ['Password-Reset']

    @swagger_auto_schema(request_body=PhoneSRL, tags=['Password-Reset'])
    def post(self, request):
        data = request.data
        if data.get('phone'):
            phone = data['phone']
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                user = user.first()
                context = send_sms(phone)
                return Response(context, status=status.HTTP_208_ALREADY_REPORTED)
            return Response({'msg': _('User not found!')})
        return Response({'msg': _("Enter phone number")}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordVerifyCode(VerifyCodeView):
    my_tags = ['Password-Reset']

class ResetPasswordConfirm(APIView):
    permission_classes = [AllowAny]
    parser_classes = [parsers.MultiPartParser]
    serializer_class = ResetPasswordSerializer

    @swagger_auto_schema(request_body=ResetPasswordSerializer, tags=['Password-Reset'])
    def put(self, request, *args, **kwargs):
        try:
            user = User.objects.get(phone=request.data['phone'])
        except:
            return Response({'error': "User matching query doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ResetPasswordSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            ver = Verification.objects.get(phone=request.data['phone'])
            print('Ver', ver.step_reset)
            user.set_password(request.data['new_password'])
            ver.step_reset = ''
            ver.save()
            user.save()
            return Response({'message': 'Password successfully updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePhoneNumber(APIView):
    queryset = User.objects.all()
    serializer_class = PhoneSRL
    parser_classes = [parsers.MultiPartParser]
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=PhoneSRL, tags=['Account'])
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get("phone")
        if phone_number.isdigit() and len(phone_number) > 8:
            user = User.objects.filter(phone__iexact=phone_number)
            if user.exists():
                return Response({
                    "status": False,
                    "detail": "Bu raqam avval registerdan otgan."
                })
            else:
                otp = send_sms(phone_number)
                if 'verify_code' in otp:
                    code = str(otp['verify_code'])
                    try:
                        validate = ValidatedOtp.objects.get(phone=phone_number)
                        if validate.validated:
                            validate.otp = code
                            validate.validated = False
                            validate.save()
                        else:
                            pass

                    except ValidatedOtp.DoesNotExist as e:
                        phon = ValidatedOtp.objects.filter(phone__iexact=phone_number)
                        if not phon.exists():
                            ValidatedOtp.objects.create(phone=phone_number, otp=code, validated=False)
                        else:
                            Response({"phone": "mavjud"})

                return Response({
                    "status": True,
                    "detail": "SMS xabarnoma jo'natildi",
                    "code": otp  # <--vaqtinchalik qo'shildi
                })
        else:
            if len(phone_number) < 8:
                return Response({"detail": "Telefon raqamingizni kod bilan kiriting!"})
            else:
                return Response({
                    "status": False,
                    "detail": "Telefon raqamni kiriting ."
                })


class ChangePhoneNumberVerifyCode(APIView):
    my_tags = ['Account']
    serializer_class = VerifyCodeSerializer
    permission_classes = [AllowAny]
    parser_classes = [parsers.MultiPartParser]
    queryset = Verification.objects.all()

    @swagger_auto_schema(request_body=VerifyCodeSerializer, tags=['Account'])
    def put(self, request, *args, **kwargs):
        data = request.data
        try:
            obj = Verification.objects.get(phone=data['phone'])
            serializer = VerifyCodeSerializer(instance=obj, data=data)
            if serializer.is_valid():
                serializer.save()
                if serializer.data['step_change_phone'] == 'confirmed':
                    user = request.user
                    user.phone = data['phone']
                    user.save()
                    return Response({'message': 'Your phone number has been successfully changed!'},
                                    status=status.HTTP_202_ACCEPTED)
                return Response({'message': 'This phone number has been successfully verified!'},
                                status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Verification.DoesNotExist:
            return Response({'error': 'Phone number or verify code incorrect!'},
                            statusis_pupil=status.HTTP_400_BAD_REQUEST)



class ChangePhoneNumberConfirm(APIView):
    permission_classes = [AllowAny]
    parser_classes = [parsers.MultiPartParser]
    serializer_class = PhoneSRL

    @swagger_auto_schema(request_body=PhoneSRL, tags=['Account'])
    def put(self, request, *args, **kwargs):
        try:
            user = User.objects.get(phone=request.user)
        except:
            return Response({'error': "User matching query doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PhoneSRL(instance=user, data=request.data)
        if serializer.is_valid():
            ver = Verification.objects.get(phone=request.data['phone'])
            user.phone = request.data['phone']
            user.save()
            ver.step_reset = ''
            ver.delete()

            updated_user = User.objects.get(phone=serializer.data['phone'])
            access_token = AccessToken().for_user(updated_user)
            refresh_token = RefreshToken().for_user(updated_user)

            return Response({'message': 'Phone successfully updated',
                             'access': str(access_token),
                             'refresh': str(refresh_token),
                             })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserOrderPostView(APIView):
    parser_classes = [parsers.MultiPartParser, ]

    @swagger_auto_schema(request_body=OrderSerializer)
    def post(self, request, id):
        product = Product.objects.filter(id=id).first()
        quantity = int(request.data['quantity'])
        if product.quantity > 0 and product.quantity >= quantity:
            serializers = OrderSerializer(data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data)
            else:
                return Response(serializers.errors)
        else:
            return Response("Bizda bu mahsulot hozircha yetarli emas")

            





class Korzinka(APIView):
    parser_classes = [parsers.MultiPartParser]

    def get(self, request, pk):
        user = User.objects.filter(id = pk).first()
        if user:
            orders = Order.objects.filter(user=user)
            sum_all = 0
            sum_cre = 0
            products = []
            qomagan = []
            for order in orders:
                if order.payment == "naqt":
                    prod = order.product
                    product = Product.objects.filter(id=prod.id).first()
                    name = ProductInfo.objects.get(product=prod.id).name
                    product_instance = ProductInfo.objects.get(product=prod.id)
                    if product_instance:
                        if order.pro_x == "is_buy":
                            if order.quantity <= product.quantity:
                                sum_all += int(product.cost) * int(order.quantity)
                                serializer = OrderSerializer(order)
                                seri = ProducInfoSerializer(product_instance)
                            else:
                                qma = ProducInfoSerializer(product_instance)
                                qomagan.append(qma)
                    products.append(seri.data)
                else:
                    prod = order.product
                    product = Product.objects.filter(id=prod.id).first()
                    name = ProductInfo.objects.get(product=prod.id).name
                    product_instance = name
                    if product_instance:
                        if order.pro_x == "is_buy":
                            if order.quantity <= product.quantity:
                                sum_cre += (int(product.cost)*(1 + int(product.prosent)) * int(order.quantity))/int(order.oy_cre)
                                serializer = OrderSerializer(order)
                                seri = ProducInfoSerializer(product_instance)
                            else:
                                qma = ProducInfoSerializer(product_instance)
                                qomagan.append(qma)
                    products.append(seri.data)
            return Response({
                            "sum_all":str(sum_all),
                            "sum_cre":str(sum_cre),
                            "data":serializer.data,
                             "product":products,
                            "Bizda yoq":qomagan
                             })

        else:
            return Response("Siz hali ro'yhatdan o'tmagansiz")

class StatausOrderView(APIView): # rasmiylashtirish orderni shunda orderni ustiga bosadi tipa order post
    @swagger_auto_schema(request_body=OrderSerializer)
    def patch(self, request, pk):
        order = Order.objects.filter(id = pk).first()
        if order:
            if order.payment == "naqt":
                serializer = OrderCashSerializer(instance=order, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"data":serializer.data, 'msg':"hozircha shu"})
                    # params = {
                    #                 'type':"to'lov",
                    #                 'user':str(user.name),
                    #                 'card':str(card),
                    #                 'payment':payment
                    #             }
                    # response = requests.post(api_url=api_url, header=header, params=params)
                    # if response.status_code == 200:
                    #     order.stat = 'buyurtma_tayyorlanmoqda'
                    #     order.save()
                    #     seri = OrderSerializer(order)
                    #     return Response({"data":seri.data, "status":status_payment})
                    # else:
                    #     return Response("Birozdan keyin urinib ko'ring")
                else:
                    return Response({'error':serializer.errors, "msg":"to'lov qismida xatolik mavjud"})

            elif order.payment == "credit":
                serializers = OrderPaySerializer(instance=order, data=request.data, partial=True)
                if serializers.is_valid():
                    serializers.save()
                    if order.tasdiq is not None:
                        if order.tasdiq == True:
                            order.stat = 'buyurtma_tayyorlanmoqda'
                            order.save()
                            seri = OrderSerializer(order)
                            return Response({"data":seri.data, "msg":"ushbu buyurtma uchun kredit muvafqiyatli ajratildi"})
                        else:
                            return Response("Ushbu tovar uchun kredit ajratilmadi")
                    else:
                        return Response("Admin tasdiqlashini kuting")
                else:
                    return Response({"error":serializers.errors, 'msg':"to'lov qismida xatolik mavjud"})
            else:
                return Response("xatolik mavjud, to'liv turini tanlang")
        else:
            return Response('Hozircha burutmalar topilmadi')



class IsLikeView(APIView):

    def get(self, request, pk):
        user = User.objects.filter(id=pk).first()
        if user:
            order = Order.objects.filter(user=user.id).first()
            if order:
                product = Product.objects.filter(id=order.product.id).first()
                pro_info = ProductInfo.objects.filter(product=product).first()
                if order.pro_x == "is_like":
                    date = d.datetime.today()
                    time = request.data.get('time')
                    if time is None:
                        return Response("Vaqt?")

                    try:
                        time = d.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        return Response("Vaqt formati: 'YYYY-MM-DD HH:MM:SS' .")

                    if date < time:
                        serializer = OrderSerializer(order)
                        seri = ProducInfoSerializer(pro_info)
                        return Response({"data": serializer.data,
                                         "product": seri.data})
                    else:
                        return Response('Korzinka avtomat tarzda tozalandi')
            else:
                return Response("Sizda hozircha mahsulotlar mavjud emas!")
        else:
            return Response("Siz hali ro'yhatdan o'tmagansiz")









# burutma berildi
# order naqt da paymentdan statsu kelsa buyurtma_qabul qilindi
# agar credit summa 3mln dan kam bo'lsa ish joy kkmas
# order creditda admin tasdiqlasa buyurtma_qabul qilindi




