from django.db import models
from django.contrib.auth.models import User


class CommonData(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=8000)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Posts(CommonData):
    title = models.CharField(max_length=150)


class Comments(CommonData):
    under_post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    reply_to = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
