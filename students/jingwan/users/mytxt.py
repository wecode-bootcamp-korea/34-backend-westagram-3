import json
import bcrypt

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError

from users.models           import User
from users.validator        import (
    username_validate,
    email_validate,
    password_validate,
    phone_number_validate
)

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
            
            username_validate(username)
            email_validate(email)
            phone_number_validate(phone_number)
            password_validate(password)

            __password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode(utf)

            if User.objects.filter(username = username).exists():
                return JsonResponse({'message' : 'Duplicated_Username'} , status = 400)
            
            if User.objects.filter(phone_number = phone_number).exists():
                return JsonResponse({'message' : 'Duplicated_PhoneNumber'} , status = 400)
            
            if User.objects.filter(email = email).exists():
                return JsonResponse({'message' : 'Duplicated_Email'} , status = 400)    
            
            User.objects.create(
                username     = username ,
                first_name   = first_name ,
                last_name    = last_name ,
                email        = email ,
                password     = __password ,
                phone_number = phone_number
            )

            return JsonResponse({'message' : 'SUCCESS'} , status = 201)
            
        except KeyError:
            return JsonResponse({'message' : 'Key_Error'} , status = 400)
            
        except ValidationError as erorr:
            return JsonResponse({'message' : erorr.message}, status = 400)

class LogInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            username = data['username']
            password = data['password']

            if not User.objects.filter(username = username).exists():
                return JsonResponse({"message" : "INVALID_USER"}, status = 401)
            
            if User.objects.get(username = username).password != password:
                return JsonResponse({"message" : "INVALID_USER"}, status = 401)
                
            return JsonResponse({'message' : 'SUCCESS'} , status = 200)

        except KeyError:
            return JsonResponse({'message' : 'Key_Error'} , status = 400)