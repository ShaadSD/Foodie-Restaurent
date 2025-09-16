from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet,SpecialViewset,CategoryViewset,ReviewViewSet


router = DefaultRouter()
router.register('items',ItemViewSet)
router.register('categories',CategoryViewset)
router.register('special-offers',SpecialViewset)
router.register('review',ReviewViewSet,basename='review')

urlpatterns = [
    path('',include(router.urls)),
]

