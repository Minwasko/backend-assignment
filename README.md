
#To deploy the application:

Clone the repository\
You should be at ```backend-assignment/products_backend```\
Install the packages:\
```pip install django```\
```pip install djangorestframework```\
```pip install django-filtger```\
To start the app:\
```python manage.py runserver```\
the app should then be available at http://127.0.0.1:8000/

if for some reason it doesn't work with the database in the repository, you can delete the existing one and do\
```python manage.py migrate```\
to have a fresh one, but it will be empty.

To run the tests\
```python manage.py test products.tests```
#Assignment API endpoints

List of all categories: ```http://127.0.0.1:8000/categories```

List of products of some category: ```http://127.0.0.1:8000/categories/{category_id}```

Create a category:\
```POST http://127.0.0.1:8000/categories | body={"name": "category name"}```

Update a category:\
```PUT http://127.0.0.1:8000/categories/{category_id} | body={"name": "new category name"}```

Delete a category:\
```DELETE http://127.0.0.1:8000/categories/{category_id}```

Create a product:\
```POST http://127.0.0.1:8000/products | body={"name": "product name", "category": category_id}```

Update a product:\
```PUT http://127.0.0.1:8000/products/{product_id} | body={"name": "updated name", "category": new_category_id}```

Delete a product:\
```DELETE http://127.0.0.1:8000/products/{product_id}```