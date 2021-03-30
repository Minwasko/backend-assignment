# backend-assignment

To deploy the application:\
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

to run the tests\
```python manage.py test products.tests```