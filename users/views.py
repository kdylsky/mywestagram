import json
import re
import bcrypt
import jwt

from django.views import View
from django.http import JsonResponse
from django.conf import settings

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

            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            User.objects.create(
                name            = name,
                email           = email,
                password        = hashed_password,
                phone_number    = phone_number
            )

            return JsonResponse({"message":"성공"}, status=200)

        except KeyError:
            return JsonResponse({"message":"키에러"}, status=400)
        except ValueError as e:
            return JsonResponse({"message":f"{e}"}, status=400)

class SignInView(View):
    def post(self,request):
        try:
            data        = json.loads(request.body)
            email       = data["email"]
            password    = data["password"]
            user        = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                return JsonResponse({"message":"잘못된 비밀번호 입니다."}, status=400)

            access_token = jwt.encode({"id":user.id}, settings.SECRET_KEY, settings.ALGORITHM)
            return JsonResponse(
                {"message":"로그인에 성공하였습니다.",
                "access_token": access_token},
                status=200
            )

        except User.DoesNotExist:
            return JsonResponse({"message":"존재하지 않는 이메일입니다."}, status=400)
        except KeyError:
            return JsonResponse({"message" : "키에러"}, status=400)


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
