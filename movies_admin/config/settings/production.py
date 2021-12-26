from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'moviesdb',
        'USER': 'userdb',
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': 5432,
        'OPTIONS': {
                   'options': '-c search_path=public,content'
        }
    }
}
