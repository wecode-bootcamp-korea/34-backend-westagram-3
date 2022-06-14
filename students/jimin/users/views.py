import json
import re
import bcrypt

from django.http     import JsonResponse
from django.views    import View

from users.models    import User
# Create your views here.

class SignUpView(View):
    def post(self, request):
        try :
             data         = json.loads(request.body)
             email        = data['email']
             password     = data['password']
             phone_number = data['phone_number']
             first_name   = data['first_name']
             last_name    = data['last_name']
             
             REGEX_EMAIL        = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$' #(소문자 a~z, 대문자 A~Z, 숫자 0~9, +-_.) + @ + .
             REGEX_PASSWORD     = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,25}$'
             REGEX_PHONE_NUMBER = '\d{3}-\d{4}-\d{4}'
             REGEX_LAST_NAME    ='^[a-zA-Z가-힣]+$'
             REGEX_FIRST_NAME   ='^[a-zA-Z가-힣]+$'
             
             if not re.match(REGEX_EMAIL,email):
                 return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)
             
             if not re.match(REGEX_PASSWORD,password):
                 return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)
             
             if not re.match(REGEX_PHONE_NUMBER,phone_number):
                 return JsonResponse({'message' : 'INVALID_PHONE_NUMBER'}, status = 400)
             
             if not re.match(REGEX_LAST_NAME,last_name):
                 return JsonResponse({'message' : 'INVALID_LAST_NAME'}, status = 400)
             
             if not re.match(REGEX_FIRST_NAME,first_name):
                 return JsonResponse({'message' : 'INVALID_FIRST_NAME'}, status = 400)
             
             if User.objects.filter(email=email).exists():
                 return JsonResponse({'message': 'DUPLICATE_EMAIL'}, status=400)
             
            
             decoded_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
             
             User.objects.create(
                first_name   = data['first_name'],
                last_name    = data['last_name'],
                email        = data['email'],
                password     = decoded_password,
                phone_number = data['phone_number'],
            )
             
             return JsonResponse({'message' : 'SUCCESS'}, status=201)
        except KeyError:
             return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class SignInView(View):
    def post(self, request):
        try :
            data = json.loads(request.body)
            
            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "INVALID_USER"}, status=401)
            else :
                user = User.objects.get(email = data['email'])
            
            if user.password != data['password']:
                return JsonResponse({"message": "INVALID_USER"}, status=401)
            
            
            return JsonResponse({'message' : 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)