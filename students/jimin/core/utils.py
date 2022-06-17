import bcrypt
import jwt

from django.http     import JsonResponse

from users.models    import User
from westagram.settings import SECRET_KEY,ALGORITHM             


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            assess_token = request.headers.get('Authorization',None) # HTTP request의 헤더 Authorization 값 가져오는데 없으면 None
            payload = jwt.decode(assess_token, SECRET_KEY, ALGORITHM) # payload:토큰을 디코딩하면 나오는 사용자정보 / 동일한 사용자라면 동일한 payload가 반환
            user = User.objects.get(email=payload['email']) # payload와 매치되는 사용자 정보를 HTTP request user에 저장
            request.user = user
            return func(self, request, *args, **kwargs)

        except jwt.exceptions.InvalidSignatureError: # 토큰의 서명이 토큰의 일부로 제공된 서명과 일치하지 않을 때 
            return JsonResponse({'message': 'INVALID_SIGNATURE_ERROR'}, status=400)

        except jwt.exceptions.DecodeError: # 없는 토큰 값이 들어왔을 때
            return JsonResponse({'message': 'DECODE_ERROR' }, status=400)

        except User.DoesNotExist: # User 테이블에 매치되는 값이 없을 때
            return JsonResponse({'message': 'USER_DOES_NOT_EXIST_ERROR'}, status=400)

        except jwt.exceptions.ExpiredSignatureError: # 토큰의 exp클레임이 만료되었음을 나타낼 때 
            return JsonResponse({"message": "EXPIRED_TOKEN"}, status=400)
    return wrapper