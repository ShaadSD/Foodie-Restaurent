from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from food.models import Item

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    total = models.PositiveIntegerField()
    date  = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Cart ({self.user.username})"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity = models.IntegerField()
    subtotal = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.item.name}"




ORDER_STATUS =(
    ("Complete","Complete"),
    ("Order Processing","Order Processing"),
    ("Order Canceled","Order Canceled")
)

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True)
    payment=models.CharField(default="Cash on delivery")
    address = models.CharField(max_length=225)
    phone = models.CharField(max_length=16, default='01700000000')
    first_name = models.CharField(max_length=16, null=True)
    last_name = models.CharField(max_length=16)
    email = models.CharField(max_length=30)
    delivery = models.PositiveIntegerField()
    total = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(choices=ORDER_STATUS,max_length=100,default="Order Processing")


class OrderedItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='ordered_items')
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    