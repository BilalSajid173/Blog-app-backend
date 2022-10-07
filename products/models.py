from email.policy import default
from django.db import models
from account.models import User
# Create your models here.


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    imageId = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    commentCount = models.IntegerField(null=True, default=0)
    likesCount = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.title
