import json
import jwt
import re

from django.http import JsonResponse
from django.views import View
from django.conf import settings

from .models import Post
from users.models import User

class PostingView(View):
    def post(self, request):
        try:
            body_data    = json.loads(request.body)
            # head_data    = json.loads(request.headers)

            # access_token = head_data.get('authorization')

            # user         = User.objects.get(id=jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM )["id"])
            user = User.objects.get(id=9)
            image        = body_data["image_url"]
            content      = body_data["content"]

            # check_image()
            Post.objects.create(
                user    = user,
                image   = image,
                content = content
            )

            return JsonResponse({"message": "게시물을 등록합니다."}, status=200)

        except KeyError :
            return JsonResponse({"message": "keyerror"}, status=400)

        except ValueError as e:
            return JsonResponse({"message": f"{e}"}, status=400)

def check_image(image):
    image_pattern = '^(http\:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(?:\/\S*)?(?:[a-zA-Z0-9_])+\.(?:jpg|jpeg|gif|png))$'
    if not re.match(image_pattern, image):
        raise ValueError("잘못된 이미지 주소입니다.")