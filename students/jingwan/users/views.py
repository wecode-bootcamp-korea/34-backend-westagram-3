import json

from django.http      import JsonResponse
from django.views     import View

from users.models     import User
from users.validator  import *

class SingUpView(View):
    def post(self, request):
        try:
            data             = json.loads(request.body)
            username         = data['username']
            first_name       = data['first_name']
            last_name        = data['last_name']
            email            = data['email']
            password         = data['password']
            phone_number     = data['phone_number']
            
            not_found(data)
            username_validate(username)
            email_validate(email)
            phone_number_validate(phone_number)
            password_validate(password)

            User.objects.create(
                username     = username ,
                first_name   = first_name ,
                last_name    = last_name ,
                email        = email ,
                password     = password ,
                phone_number = phone_number
            )

            return JsonResponse({'message' : 'SUCCESS'} , status = 201)
        except KeyError:
            return JsonResponse({'message' : 'KeyError'} , status = 400)
        except:
            return JsonResponse(result, status = 400)

class LogInView(View):
    def post(self, request):
        try:
            data      = json.loads(request.body)
            username  = data['username']
            password  = data['password']

            if not User.objects.filter(username = username, password = password).exists():
                return JsonResponse({"message" : "INVALID_USER"}, status = 401)
            
            return JsonResponse({'message' : 'SUCCESS'} , status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KeyError'} , status = 400)