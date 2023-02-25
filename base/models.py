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
    host_profile = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to='post_images',null=True,blank=True)
    caption =models.TextField(null=True, blank=True)
    created =models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    no_of_likes = models.IntegerField(default=0)



    class Meta:
        ordering = ['-created']


    def __str__(self) -> str:
        return self.user.username



class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.username
    


class FollowerCount(models.Model):
    followers = models.CharField(max_length=200)
    user = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.user
    


class Comment(models.Model):
    
    comment_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    post_comment = models.TextField()


    def __str__(self) -> str:
        return self.comment[0:50]