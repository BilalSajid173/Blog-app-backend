from django.db import models
from account.models import User
# Create your models here.


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    imageId = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    commentCount = models.IntegerField(null=True, default=0)
    likesCount = models.IntegerField(null=True, default=0)
    tags = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likesCount = models.IntegerField(null=True, default=0)
    dislikesCount = models.IntegerField(null=True, default=0)
