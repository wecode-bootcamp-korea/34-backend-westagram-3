import re

from users.models import User

EMAIL_REGEX         = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
PHONE_NUMBER_REGEX  = '\d{3}-\d{3,4}-\d{4}'
PASSWORD_REGEX      = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
result              = {'message': None}
     
def not_found(data):
    for key,value in data.items():
        if bool(value) == False:
            result['message'] = f'{key}NotFound'
            raise
         
def username_validate(username):
    if User.objects.filter(username = username).exists():
        result['message'] = 'UsernameDuplicate'
        raise
         
def email_validate(email):
    if User.objects.filter(email = email).exists():
        result['message'] = 'EmailDuplicate'
        raise
    elif not re.match( EMAIL_REGEX, email):
        result['message'] = 'InvalidEmail'
        raise
 
def password_validate(password):
    if not re.match( PASSWORD_REGEX, password):
        result['message'] = 'InvalidPassword'
        raise

 
def phone_number_validate(phone_number):
    if User.objects.filter(phone_number = phone_number).exists():
        result['message'] = 'PhoneNumberDuplicate'
        raise
    elif not re.match( PHONE_NUMBER_REGEX ,phone_number):
        result['message'] = 'InvalidPhoneNumber'
        raise