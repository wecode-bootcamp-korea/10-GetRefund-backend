import json
import jwt
import bcrypt
import re
import datetime

from django.views import View
from django.http  import HttpResponse, JsonResponse

from .models      import User             

import my_settings


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message': 'EMAIL_ALREADY_EXISTS'}, status=400) 

            if '@' or '.' not in data['email']:
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
                      
                    return JsonResponse({'Access_Token':access_token}, status=200)

                else:
                    return JsonResponse({'message':'UNAUTHORIZED'}, status=401)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
            
