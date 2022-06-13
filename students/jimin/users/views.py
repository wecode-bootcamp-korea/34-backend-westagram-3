import json ,re

from django.http     import JsonResponse
from django.views    import View


from users.models    import User
# Create your views here.

class SignUpView(View):
    def post(self, request):
        try :
             data          = json.loads(request.body)
             email         = data['email']
             password      = data['password']
             phone_number  = data['phone_number']
             
             
            
             regex_email        = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$' #(소문자 a~z, 대문자 A~Z, 숫자 0~9, +-_.) + @ + .
             regex_password     = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,25}$'
             regex_phone_number = '\d{3}-\d{4}-\d{4}'
             if not email or not password:
                 return JsonResponse({'message':'KEY_ERROR'})
             if not re.match(regex_email,email):
                 return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)
             if not re.match(regex_password,password):
                 return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)
             if not re.match(regex_phone_number,phone_number):
                 return JsonResponse({'message' : 'INVALID_PHONE_NUMBER'}, status = 400)
             if User.objects.filter(email=email).exists():
                 return JsonResponse({'message':'DUPLICATE_EMAIL'}, status=400)
            
             User.objects.create(
                first_name    = data['first_name'],
                last_name     = data['last_name'],
                email         = data['email'],
                password      = data['password'],
                phone_number  = data['phone_number'],
            )
             
             return JsonResponse({'message' : '회원 가입 완료'}, status=201)
        except KeyError:
             return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
  