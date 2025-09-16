from django.shortcuts import render
from rest_framework import viewsets,filters
from .models import Item,Category,SpecialOffer
from .serializers import ItemSerializers,CategorySerializers,SpecialOfferSerializers
import django_filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Review
from .serializers import ReviewSerializer
from rest_framework.response import Response
# Create your views here.

class ItemFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug',lookup_expr='iexact')
    permission_classes =[AllowAny]
    class Meta:
        model = Item
        fields = ['category']




class ItemPagination(PageNumberPagination):
    permission_classes =[AllowAny]
    page_size = 6
    page_query_param = "page"
    max_page_size = 10

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializers
    filterset_class = ItemFilter
    pagination_class = ItemPagination
    permission_classes =[AllowAny]
    filter_backends =[DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['name','category__name','description']
    ordering_fields = ['price']   
    ordering = ['-price'] 


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [AllowAny]

class SpecialViewset(viewsets.ModelViewSet):
   
    queryset = SpecialOffer.objects.all()
    serializer_class = SpecialOfferSerializers
    permission_classes = [AllowAny]


    
class ReviewViewSet(viewsets.ViewSet):
    permission_classes =[AllowAny]
    def list(self, request):
        query = Review.objects.all()
        serializer = ReviewSerializer(query, many=True)
        return Response(serializer.data)

    def create(self, request):
        review_title = request.data['review_title']
        content = request.data['content']

        Review.objects.create(
            user_name=request.user.first_name,
            review_title=review_title,
            content=content,
        )

        return Response({"message": "Review created successfully"})

        
