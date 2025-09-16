from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# class Customer(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     image = models.ImageField(upload_to="profile/")
#     phone = models.IntegerField(max_length=11)
#     def __str__(self):
#         return self.user.username



class ContactUs(models.Model):
    name=models.CharField(max_length=40)
    email=models.CharField(max_length=50)
    message=models.TextField()
    
    def __str__(self):
        return self.email
    class Meta:
        verbose_name_plural="Contact Us"
