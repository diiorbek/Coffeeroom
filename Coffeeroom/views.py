from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

import django_filters
from .models import Product, Category, Branch
from .serializers import ProductSerializer, CategorySerializer, BranchSerializer

class ReadOnlyModelViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
 
class ProductFilter(django_filters.FilterSet):
    branch_id = django_filters.CharFilter(field_name="category__branch__id", lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['branch_id']

class CategoryFilter(django_filters.FilterSet):
    branch_id = django_filters.CharFilter(field_name="branch_id", lookup_expr='exact')

    class Meta:
        model = Category
        fields = ['branch_id']

class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all() 
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    class Meta:
        tags = ["Products"]


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CategoryFilter
    class Meta:
        tags = ["Categories"]

class BranchViewSet(ReadOnlyModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    filter_backends = (DjangoFilterBackend,)
    class Meta:
        tags = ["Branches"] 
        
