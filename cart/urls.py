from django.urls import path,include
from .views import Delatefullcart,MyCart,OrderViewset, DereaseCartItem, IncreaseCartItem, AddToCartViewset, DeleteCartItem
from rest_framework import routers

router = routers.DefaultRouter()

router.register('cart',MyCart,basename ="MyCart")
router.register('order',OrderViewset,basename ="order_history")


urlpatterns = [
    path('', include(router.urls)),
    path('increase/',IncreaseCartItem.as_view(),name='increase'),
    path('decrease/',DereaseCartItem.as_view(),name='decrease'),
    path('full_delete/',Delatefullcart.as_view(),name='full_delete'),
    path('add_to_cart/',AddToCartViewset.as_view(),name='add_to_cart'),
    path('delete_cart/',DeleteCartItem.as_view(),name='delete_cart'),
   
]
