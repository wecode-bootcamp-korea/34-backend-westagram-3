import json ,re

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
             '''
             if User.ojects.filter(email=data['email']).exists():
                 return JsonResponse({'message':'Duplicate Email'}, status=400)
             '''
             regex_email    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$' #(소문자 a~z, 대문자 A~Z, 숫자 0~9, +-_.) + @ + .
             regex_password = '\S{8,25}' #8자이상 25자이하
             
             if not re.match(regex_email,email):
                 return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)
             if not re.match(regex_password,password):
                 return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)
             
             User.objects.create(
                first_name    = data['first_name'],
                last_name     = data['last_name'],
                email         = data['email'],
                password      = data['password'],
                phone_number  = data['phone_number'],
            )
             
             return JsonResponse({'message' : 'SUCCESS'}, status=201)
        except KeyError:
             return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
  