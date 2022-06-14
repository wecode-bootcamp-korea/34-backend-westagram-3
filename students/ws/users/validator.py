import re

def validate_email(email):
    EMAIL_REGEX = re.match('^[a-zA-z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.]+$', email)
    return EMAIL_REGEX

def validate_password(password):
    PASSWORD_REGEX = re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$', password)
    return PASSWORD_REGEX