from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.CharField(max_length=100)
    date=models.DateTimeField( auto_now_add=True)
    likes=models.ManyToManyField(User,blank=True,related_name="liked_byusers")

    def serialize(self):
        return {
            "id": self.id,
            "user":self.user.username,
            "content": self.content,
            "date": self.date.strftime("%b %#d %Y, %#I:%M %p"),
            "likes": [user.username for user in self.likes.all()]

        }

class Follow(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    followers=models.ManyToManyField(User,blank=True,related_name="followers")
    following=models.ManyToManyField(User,blank=True,related_name="following")





