import json

from django.http     import JsonResponse
from django.views    import View

from users.models    import User
from users.validator import validate_email, validate_password

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

            validate_email(email)
            validate_password(password)

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

            return JsonResponse({"message": "SIGHUP SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse( {"message" : "KEYERROR"}, status = 400)