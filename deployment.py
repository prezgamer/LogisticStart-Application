import os
from .settings import *
from .settings import BASE_DIR

#which domain can be used by this code (only azure url can be used for this code)
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]
#specify which domain can access our application
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']]
#Do not use debug mode in production as it will expose sensitive information like paths directories
DEBUG = False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

conn_str = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres', 
        'USER': 'postgres.czpozqdxdrqxotrqpavt', 
        'PASSWORD': 'SnBZzPjqg@yqgp5', 
        'HOST':'aws-0-ap-southeast-1.pooler.supabase.com',
        'PORT':'5432',
    }
}