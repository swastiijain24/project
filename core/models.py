import uuid
from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()

class Profile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    bio =models.TextField(blank=True)
    profileimg =models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location =models.CharField(max_length=255, null=True)
    workingat=models.CharField(max_length=255, null=True)
    education= models.CharField(max_length=255, null=True)
    bgimg = models.ImageField(upload_to='bgimg', default='defbgimg.png')
    follower_count=models.IntegerField(default=0)
    following_count=models.IntegerField(default=0)

    def __str__(self):
        return self.user_id.username

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='userpost')
    image = models.ImageField(upload_to='posts')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    no_of_likes = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name='posts')

    def __str__(self):
        return self.profile_id.user_id.username
    
class LikePost(models.Model):
    post_id=models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
class Follow(models.Model):
    username=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user')
    followperson=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followperson')