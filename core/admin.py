from django.contrib import admin
from .models import LikePost, Post, Profile, Follow, Tag

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(Follow)
admin.site.register(Tag)