import json
import jwt
import bcrypt
import re
import datetime

from django.views import View
from django.http  import HttpResponse, JsonResponse

from .models        import User             
from .utils         import login_decorator
from order.models   import Order, OrderStatus
from product.models import Product

import my_settings


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message': 'EMAIL_ALREADY_EXISTS'}, status=400) 

            if '@' not in data['email']:
                return JsonResponse({'message': 'INVALID_EMAIL'}, status=401)

            if len(data['password']) < 8:
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)

            User.objects.create(
                first_name  = data['first_name'],
                last_name   = data['last_name'],
                birthday    = datetime.datetime.strptime(data['birthday'], '%Y.%m.%d').date(),
                email       = data['email'],
                password    = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                )
                
            return JsonResponse ({'message':'SIGNUP_SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse ({'message':'INVALID_KEY'}, status=401)


class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email=data['email'])

                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    access_token = jwt.encode({'user_id':user.id}, my_settings.SECRET_KEY['secret'], my_settings.ALGORITHM['algorithm']).decode('utf-8')
                      
                    return JsonResponse({'access_token':access_token}, status=200)

                else:
                    return JsonResponse({'message':'UNAUTHORIZED'}, status=401)
            else:
                return JsonResponse({'message':'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


class MyOrder(View):
    @login_decorator
    def post(self, request):
        ordered_items = Order.objects.filter(order_status_id=1)

        for ordered_item in ordered_items:
            ordered_item.order_status_id=3
            ordered_item.save()

        return JsonResponse ({'message':'ORDER_COMPLETE'}, status=200)

    @login_decorator
    def get(self, request):

        ordered_items = []
        order_items = Order.objects.filter(user_id=request.user.id, order_status_id=3).select_related("order_status").prefetch_related("product")
        
        for item in order_items:
            data = {
                "name" : item.product.name,
                "price" : item.product.price,
                "quantity" : item.quantity,
                "color" : item.product.color.name,
                "order_status" : item.order_status.name,
                "image" : item.product.image_set.get(image_category=1).image_url
            }
            ordered_items.append(data)

        return JsonResponse ({'MyOrder': ordered_items})


class MyPage(View):
    @login_decorator
    def get(self, request):
        return JsonResponse ({'first_name': request.user.first_name})
