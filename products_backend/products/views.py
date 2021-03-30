from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import CategorySerializer, ProductSerializer, CategoryListSerializer, ProductCreateSerializer
from .models import Category, Product
from django_filters.rest_framework import DjangoFilterBackend

# here I've decided to show different ways of setting views, categories are done through simple functions,
# products are done using implemented classes


@api_view(['GET', 'POST'])
def get_post_categories(request):
    if request.method == 'POST':
        serializer = CategoryListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def get_put_delete_category(request, pk):
    try:
        db_category = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(db_category)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CategoryListSerializer(db_category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        db_category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']  # this line here allows us to filter products based on category id
    # "/products?category=2", alternatively you can view which products belong to category by "categories/2"
    # where 2 is category id

    def create(self, request, *args, **kwargs):
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def put(self, request, *args, **kwargs):
        try:
            db_product = Product.objects.get(id=kwargs['pk'])
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductCreateSerializer(db_product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            db_product = Product.objects.get(id=kwargs['pk'])
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        db_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)