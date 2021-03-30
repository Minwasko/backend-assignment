from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"""|{self.name}| with id={self.id}"""


# It was said, that one product may belong to one category, I am assuming here that
# each category may have multiple different products in it
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return f"""|{self.name}| with id={self.id}"""
