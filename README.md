A .env file is needed in the \data_api_app folder

It should contain:

SECRET_KEY = ''

DJANGO_SUPERUSER_USERNAME=''
DJANGO_SUPERUSER_PASSWORD=''
DJANGO_SUPERUSER_EMAIL=''


run the following command after starting the server:
python manage.py createsuperuser --noinput
