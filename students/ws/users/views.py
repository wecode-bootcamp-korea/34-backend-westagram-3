import re
import json

from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ValidationError

from users.models import User

def validate_email(email):
    EMAIL_REGEX = re.match('^[a-zA-z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.]+$', email)
    return EMAIL_REGEX

def validate_password(password):
    PASSWORD_REGEX = re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$', password)
    return PASSWORD_REGEX

class SighUpView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            username     = data['username']
            first_name   = data['first_name']
            last_name    = data['last_name']
            email        = data['email']
            password     = data['password']
            phone_number = data['phone_number']

            if not validate_email(email):
                return JsonResponse( {"message" : "INVALID_EMAIL"}, status = 400)

            if not validate_password(password):
                return JsonResponse( {"message" : "INVALID_PASSWORD"}, status = 400)
                
            if User.objects.filter(email = email).exists():
                return  JsonResponse( {"message" : "Email Already Exists"}, status = 400)

            User.objects.create(
                username     = username,
                first_name   = first_name,
                last_name    = last_name,
                email        = email,
                password     = password,                    
                phone_number = phone_number
            )

            return JsonResponse({"message": "SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse( {"message" : "KEYERROR"}, status = 400)