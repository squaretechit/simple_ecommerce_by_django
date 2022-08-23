from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=50, blank=True)
    postcode = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    profile_pic = models.ImageField(default='profile-pic.svg', upload_to='Users_Profile_pic')

    def __str__(self):
        return str(self.user.username)


class AllNotification(models.Model):
    name = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    held_by = models.CharField(max_length=255)
    view = models.BooleanField(default=False)
    notification = models.TextField()
    date = models.DateTimeField(auto_now_add=True)