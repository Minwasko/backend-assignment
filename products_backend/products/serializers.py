from rest_framework import serializers

from .models import Product, Category


# this serializer is used to describe individual products
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'category']


# this serializer is called whenever we want to create a new product or update existing one
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'category']


# this serializer is called whenever we want to see products that belong to given category
class CategorySerializer(serializers.ModelSerializer):
    products = serializers.StringRelatedField(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products']


# this serializer is here, just because when you have many products under each category, it makes it distracting, so I
# decided to divide them into different serializers for different use cases.
# this serializer is called whenever we just want a list of categories/ save a new one/ update existing one
class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
