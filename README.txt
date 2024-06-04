First:
go to settings.py in django_project folder

Create new database in mysql or mariadb

In mariadb or mysql:
Login to account
CREATE DATABASE logisticsdb;

django_project/settings.py: Line 76
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'logisticsdb', # change to your own
        'USER': '', # your own user name
        'PASSWORD': '', # change to your own password for account
        'HOST':'localhost', # no need to change
        'PORT':'3306', # change if nessary
    }
}

To run: 
cd django_web_project
cd django_project
python manage.py makemigrations
python manage.py migrate
python manage.py runserver