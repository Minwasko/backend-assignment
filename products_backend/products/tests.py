from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from .models import Category, Product
from .serializers import CategoryListSerializer, CategorySerializer, ProductSerializer, ProductCreateSerializer

client = Client()


class CategoryTests(TestCase):

    def setUp(self):
        Category.objects.create(id=1, name='test category 1')
        Category.objects.create(id=2, name='test category 2')

    def test_categories_strings_are_ok(self):
        first_category = Category.objects.get(name='test category 1')
        second_category = Category.objects.get(name='test category 2')
        self.assertEqual(str(first_category), "|test category 1| with id=1")
        self.assertEqual(str(second_category), "|test category 2| with id=2")

    def test_get_invalid_category(self):
        response = client.get('/categories/10000')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_categories(self):
        response = client.get('/categories')
        setup_categories = Category.objects.all()
        serializer = CategoryListSerializer(setup_categories, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_categories_can_be_saved(self):
        client.post('/categories', {'name': 'api category'})
        response = client.get('/categories/3')  # id is 3 since we have 2 objects saved in setUp function
        self.assertEqual(response.data, {'id': 3, 'name': 'api category', 'products': []})

    def test_categories_can_be_updated(self):
        client.post('/categories', {'name': 'api category'})
        response = client.get('/categories/3')  # id is 3 since we have 2 objects saved in setUp function
        self.assertEqual(response.data, {'id': 3, 'name': 'api category', 'products': []})

        response = client.put('/categories/3', {'name': 'api category changed'}, content_type='application/json')
        self.assertEqual(response.data, {'id': 3, 'name': 'api category changed'})

    def test_categories_can_be_deleted(self):
        response = client.get('/categories')
        self.assertEqual(len(response.data), 2)

        client.delete('/categories/2')

        response = client.get('/categories')
        self.assertEqual(len(response.data), 1)

        response = client.get('/categories/2')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_one_product_under_category_db(self):
        category3 = Category.objects.create(id=3, name='test category 3')
        Product.objects.create(name='product 1', category=category3)
        serializer = CategorySerializer(Category.objects.get(id=3))
        self.assertEqual(serializer.data, {'id': 3, 'name': 'test category 3', 'products': ['|product 1| with id=1']})

    def test_get_one_product_under_category_api(self):
        client.post('/products', {'id': 1, 'name': 'test product', 'category': 1})
        response = client.get('/categories/1')
        self.assertEqual(response.data, {'id': 1, 'name': 'test category 1', 'products': ['|test product| with id=1']})

    def test_get_multiple_products_under_category(self):
        category3 = Category.objects.create(id=3, name='test category 3')
        Product.objects.create(name='product 1', category=category3)
        Product.objects.create(name='product 2', category=category3)
        Product.objects.create(name='product 3', category=category3)
        # database side works
        serializer = CategorySerializer(Category.objects.get(id=3))
        self.assertEqual(serializer.data, {'id': 3, 'name': 'test category 3', 'products': ['|product 1| with id=1',
                                                                                            '|product 2| with id=2',
                                                                                            '|product 3| with id=3']})
        # api side works
        response = client.get('/categories/3')
        self.assertEqual(response.data, serializer.data)


class ProductTests(TestCase):

    def setUp(self):
        category = Category.objects.create(id=1, name='test category 1')
        Product.objects.create(id=1, name='test product 1', category=category)
        Product.objects.create(id=2, name='test product 2', category=category)

    def test_product_strings_are_ok(self):
        first_product = Product.objects.get(id=1)
        second_product = Product.objects.get(id=2)
        self.assertEqual(str(first_product), '|test product 1| with id=1')
        self.assertEqual(str(second_product), '|test product 2| with id=2')

    def test_get_invalid_product(self):
        response = client.get('/products/1000000')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_products(self):
        serializer = ProductSerializer(Product.objects.all(), many=True)
        response = client.get('/products')
        self.assertEqual(response.data, serializer.data)

    def test_filter_products_by_category(self):
        serializer = ProductSerializer(Product.objects.all(), many=True)
        response = client.get('/products?category=1')
        self.assertEqual(response.data, serializer.data)

    def test_filter_by_non_existing_category(self):
        response = client.get('/products?category=100')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_by_empty_category(self):
        Category.objects.create(id=2, name='empty category')
        response = client.get('/products?category=2')
        self.assertEqual(response.data, [])

    def test_product_can_be_saved(self):
        client.post('/products', {'name': 'saved product', 'category': 1})
        response = client.get('/products/3')  # id is 3, since the 1st two are saved in setup
        self.assertEqual(response.data, {'id': 3, 'name': 'saved product', 'category': '|test category 1| with id=1'})

    def test_product_can_be_updated(self):
        response = client.put('/products/1', {'name': 'product 1 name updated', 'category': 1},
                              content_type='application/json')
        self.assertEqual(response.data, {'name': 'product 1 name updated', 'category': 1})

    def test_product_invalid_info_wont_be_updated(self):
        response = client.put('/products/1', {},
                              content_type='application/json')  # updated/required fields missing here
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_can_be_deleted(self):
        response = client.get('/products')
        self.assertEqual(len(response.data), 2)

        client.delete('/products/2')
        response = client.get('/products')
        self.assertEqual(len(response.data), 1)

        response = client.get('/products/2')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
