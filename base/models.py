from django.db import models
from django.contrib.auth import get_user_model
import uuid

# Create your models here.

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True,null=True)
    avatar = models.ImageField(null=True, upload_to='profile_images', default='avatar.svg')
    location = models.CharField(max_length=200, blank=True)


    def __str__(self) -> str:
        return self.user.username
    



class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    host = models.ForeignKey(User,on_delete=models.CASCADE )
    #host_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')
    caption =models.TextField(null=True, blank=True)
    created =models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    no_of_likes = models.IntegerField(default=0)


    def __str__(self) -> str:
        return self.user.username
