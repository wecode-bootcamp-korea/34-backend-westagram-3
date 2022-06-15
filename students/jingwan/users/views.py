import json
import bcrypt
import jwt

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError

from users.models           import User
from westagram.settings     import SECRET_KEY, ALGORITHM
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

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

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
                password     = hashed_password ,
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
            username = data['email']
            password = data['password']
            user_id  = User.objects.get(username = username).id
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            if not User.objects.filter(username = username).exists():
                return JsonResponse({"message" : "INVALID_USER"}, status = 401)
            
            if not bcrypt.checkpw(password.encode('utf-8') , hashed_password):
                return JsonResponse({"message" : "INVALID_USER"}, status = 401)
            

            token = jwt.encode({'user_id': user_id}, SECRET_KEY, ALGORITHM)
                
            return JsonResponse({'ACCESS_TOKEN' : token} , status = 200)

        except KeyError:
            return JsonResponse({'message' : 'Key_Error'} , status = 400)