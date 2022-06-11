import json
import re

from django.http      import JsonResponse
from django.views     import View
from users.models     import User

class UserView(View):
    def post(self, request):
        try:
            data             = json.loads(request.body)
            username         = data['username']
            first_name       = data['first_name']
            last_name        = data['last_name']
            email            = data['email']
            password         = data['password']
            phone_number     = data['phone_number']

            EMAIL_REGEX = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            PHONE_NUMBER_REGEX = '\d{3}-\d{3,4}-\d{4}'
            PASSWORD_REGEX = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

            if bool(username) == False:
                return JsonResponse({'message' : 'UsernameNotFound'} , status = 400)
                
            if  User.objects.filter(username = username).exists():
                return JsonResponse({'message' : 'UsernameDuplicateError'} , status = 400)
            elif User.objects.filter(email = email).exists():
                return JsonResponse({'message' : 'EmailDuplicateError'} , status = 400)
            elif User.objects.filter(phone_number = phone_number).exists():
                return JsonResponse({'message' : 'PhoneNumberDuplicateError'} , status = 400)

            if not re.match(EMAIL_REGEX, email):
                return JsonResponse({'message' : 'EmailRegexError'} , status = 400)
            elif not re.match(PHONE_NUMBER_REGEX, phone_number):
                return JsonResponse({'message' : 'PhoneNumberRegexError'} , status = 400)
            elif not re.match(PASSWORD_REGEX, password):
                return JsonResponse({'message' : 'PasswordRegexError'} , status = 400)

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