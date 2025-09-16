from rest_framework import serializers
from .models import Item,SpecialOffer,Category,Review

class ItemSerializers(serializers.ModelSerializer):
    category_name = serializers.CharField(source = 'category.name',read_only = True)
    class Meta:
        model = Item
        fields = ['id','name','category','category_name','description','price','image']
        


class SpecialOfferSerializers(serializers.ModelSerializer):
    class Meta:
        model = SpecialOffer
        fields = ['id','id1','name','image','description','before_price','after_price']
        depth= 1

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','slug']
        depth= 1


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'