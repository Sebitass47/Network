from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

#Posts
class Posts(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=500)
    hearts = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.created_by}: {self.content}"

#Likes
class Heart(models.Model):
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='post_heart')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_heart')

#Following
class Following(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='principal')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return f"{self.user_id} siguio a {self.following}"