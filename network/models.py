from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    body = models.CharField(max_length=512)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="likes", null=True, blank=True)

    def __str__(self):
        return f'"{self.body}" by {self.poster}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    body = models.CharField(max_length=1024)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'"{self.body}" by {self.commenter}'