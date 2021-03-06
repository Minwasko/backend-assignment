"""products_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from products import views

urlpatterns = [
    path('categories', views.get_post_categories, name='get_post_categories'),
    path('categories/<int:pk>', views.get_put_delete_category, name='get_put_delete_category'),
    path('products', views.ProductListView.as_view(), name='get_post_products'),
    path('products/<int:pk>', views.ProductSingleView.as_view(), name='get_put_delete_product'),
]
