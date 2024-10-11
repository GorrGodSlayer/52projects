come setuppare il progetto django 
1. pip install django
2. django-admin startproject restaurant_app
   cd restaurant_app
3. python manage.py startapp core
python manage.py startapp menu
python manage.py startapp orders
python manage.py startapp tables
python manage.py startapp payments
4. INSTALLED_APPS = [
    # ...
    'core',
    'menu',
    'orders',
    'tables',
    'payments',
]
5. python manage.py makemigrations
python manage.py migrate
6. python manage.py createsuperuser
7. python manage.py runserver

PER USARE IL SISTEMA DI CHIAVI 
To use this system:

The owner (superuser) can generate a key by sending a POST request to /api/generate-key/.
The generated key should be securely shared with authorized users.
Users must include the key in the X-Access-Key header when making requests to protected views.
The require_valid_key decorator will check the key's validity before allowing access to the view.
