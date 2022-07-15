from django.db import models

from users.models import User

class Post(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    image        = models.CharField(max_length=200, unique=True)
    content      = models.CharField(max_length=200)
    create_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "posts"