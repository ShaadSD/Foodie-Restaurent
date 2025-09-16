from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=10)
    slug = models.SlugField()

    def __str__(self):
        return self.name



class Item(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to="food/images")
    slug = models.SlugField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    description = models.CharField(max_length =100)
    price = models.IntegerField(default = 0) 


    def __str__(self):
        return self.name


class SpecialOffer(models.Model):
    name = models.CharField(max_length=20)
    id1 = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="food/images/")
    description = models.CharField(max_length = 100)
    before_price = models.IntegerField()
    after_price = models.IntegerField(default = 0)

    def __str__(self):
        return self.name



    


class Review(models.Model):
    user_name = models.CharField(max_length=200)
    review_title = models.CharField(max_length=200)
    content = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.review_title}"

    