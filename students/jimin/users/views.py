import json
import re
import bcrypt
import jwt

from django.http     import JsonResponse
from django.views    import View

from users.models    import User
from westagram.settings import SECRET_KEY,ALGORITHM


class SignUpView(View):
    def post(self, request):
        try :
             data         = json.loads(request.body)
             email        = data['email']
             password     = data['password']
             phone_number = data['phone_number']
             first_name   = data['first_name']             
             last_name    = data['last_name']
             nick_name    = data['nick_name']
             
             REGEX_EMAIL        = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$' #(소문자 a~z, 대문자 A~Z, 숫자 0~9, +-_.) + @ + .
             REGEX_PASSWORD     = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,25}$'
             REGEX_PHONE_NUMBER = '\d{3}-\d{4}-\d{4}'
             REGEX_NAME    ='^[a-zA-Z가-힣]+$'
             
             
             if not re.match(REGEX_EMAIL,email):
                 return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)
             
             if not re.match(REGEX_PASSWORD,password):
                 return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)
             
             if not re.match(REGEX_PHONE_NUMBER,phone_number):
                 return JsonResponse({'message' : 'INVALID_PHONE_NUMBER'}, status = 400)
             
             if not re.match(REGEX_NAME,last_name):
                 return JsonResponse({'message' : 'INVALID_LAST_NAME'}, status = 400)
             
             if not re.match(REGEX_NAME,first_name):
                  return JsonResponse({'message' : 'INVALID_FIRST_NAME'}, status = 400)
             
             if User.objects.filter(nick_name = nick_name).exists():
    	         return JsonResponse({"MESSAGE":"DUPLICATE_NICKNAME"}, status=400)
          
             if User.objects.filter(email=email).exists():
                 return JsonResponse({"message":"DUPLICATE_EMAIL"}, status=400)
        
             decoded_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
             
             User.objects.create(
                first_name   = data['first_name'],
                last_name    = data['last_name'],
                email        = data['email'],
                password     = decoded_password,
                phone_number = data['phone_number'],
                nick_name    = data['nick_name']
            )
             
             return JsonResponse({'message' : 'SUCCESS'}, status=201)
        except KeyError:
             return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
   
    
class SignInView(View):
    def post(self, request):
        try :
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
            
            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "INVALID_USER"}, status=401)
        
            if not bcrypt.checkpw(password.encode('utf-8'), User.objects.get(email=data['email']).password.encode('utf-8')):
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            token = jwt.encode({'email':email}, SECRET_KEY, ALGORITHM)
                 
            return JsonResponse({'access_token' : token}, status=201)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)
    
    