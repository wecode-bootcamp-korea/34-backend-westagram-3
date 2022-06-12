import json
import re

from django.http      import JsonResponse
from django.views     import View
from users.models     import User

class RegexTool():
    EMAIL_REGEX         = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    PHONE_NUMBER_REGEX  = '\d{3}-\d{3,4}-\d{4}'
    PASSWORD_REGEX      = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
    result              = {'message': None}
    
    @staticmethod
    def not_found(data):
        for key,value in data.items():
            if bool(value) == False:
                RegexTool.result['message'] = f'{key}NotFound'
                raise

    @staticmethod        
    def username_regex(username):
        if User.objects.filter(username = username).exists():
            RegexTool.result['message'] = 'UsernameDuplicate'
            raise

    @staticmethod        
    def email_regex(email):
        if User.objects.filter(email = email).exists():
            RegexTool.result['message'] = 'EmailDuplicate'
            raise
        elif not re.match(RegexTool.EMAIL_REGEX, email):
            RegexTool.result['message'] = 'InvalidEmail'
            raise

    @staticmethod
    def password_regex(password):
        if not re.match(RegexTool.PASSWORD_REGEX, password):
            RegexTool.result['message'] = 'InvalidPassword'
            raise
    
    @staticmethod
    def phone_number_regex(phone_number):
        if User.objects.filter(phone_number = phone_number).exists():
            RegexTool.result['message'] = 'PhoneNumberDuplicate'
            raise
        elif not re.match(RegexTool.PHONE_NUMBER_REGEX ,phone_number):
            RegexTool.result['message'] = 'InvalidPhoneNumber'
            raise

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
            
            RegexTool.not_found(data)
            RegexTool.username_regex(username)
            RegexTool.email_regex(email)
            RegexTool.phone_number_regex(phone_number)
            RegexTool.password_regex(password)

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
            return JsonResponse(RegexTool.result, status = 400)