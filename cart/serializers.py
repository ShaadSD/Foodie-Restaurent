from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Cart,CartItem,Order,OrderedItem

class CartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        depth= 1


class CartItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
        depth= 1

class OrderedItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)

    class Meta:
        model = OrderedItem
        fields = ['id', 'item', 'item_name', 'price', 'quantity', 'subtotal']

class OrderSerializers(serializers.ModelSerializer):
    ordered_items = OrderedItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'