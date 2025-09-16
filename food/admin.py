from django.contrib import admin

# Register your models here.
from .models import Category, SpecialOffer, Item,Review


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("name",)}

class ItemAdmin(admin.ModelAdmin):
    list_display = ['id','name','category','description','price']

    prepopulated_fields = {"slug":("name",)}

    def description(self,obj):
        return obj.description[:20]
    
    description.short_description = "Description"

class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ['name','description','image','before_price','after_price']
   

admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(SpecialOffer, SpecialOfferAdmin)
admin.site.register(Review)
