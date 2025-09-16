from django.contrib import admin

# Register your models here.
from .models import Cart,CartItem,Order,OrderedItem


class CartAdmin(admin.ModelAdmin):
    list_display =['id','user','total','date']

class OrderAdmin(admin.ModelAdmin):
    list_display =['id','first_name','last_name','email','phone','order_status','total']

admin.site.register(Cart,CartAdmin)

admin.site.register(CartItem)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderedItem)