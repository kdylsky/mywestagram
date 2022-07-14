import json
import re

from django.views import View
from django.http import JsonResponse

from .models import User

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            name                = data["name"]
            email               = data["email"]
            password            = data["password"]
            phone_number        = data["phone_number"]

            check_email(email)
            check_password(password)
            check_phone_number(phone_number)

            User.objects.create(
                name            = name,
                email           = email,
                password        = password,
                phone_number    = phone_number
            )

            return JsonResponse({"message":"성공"}, status=200)

        except KeyError:
            return JsonResponse({"message":"키에러"}, status=400)
        except ValueError as e:
            return JsonResponse({"message":f"{e}"}, status=400)

def check_email(email):
    regx_email = '^[a-zA-Z0-9+-\_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not User.objects.filter(email=email).exists():
        if not re.compile(regx_email).match(email):
            raise ValueError("잘못된 이메일 형식입니다.")
    else:
        raise ValueError("이미 존재하는 이메일입니다.")

def check_password(password):
    regx_password       = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[@!%*#?&])[A-Za-z\d@!%*#?&]{8,}$'
    if not re.compile(regx_password).match(password):
        raise ValueError("잘못된 패스워드 형식입니다.")

def check_phone_number(phone_number):
    regx_phone_number = '^\d{3}-\d{3,4}-\d{4}$'
    if not User.objects.filter(phone_number=phone_number).exists():
        if not re.compile(regx_phone_number).match(phone_number):
            raise ValueError("잘못된 전화번호 형식입니다.")
    else:
        raise ValueError("이미 존재하는 휴대번호입니다.")
