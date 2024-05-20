from .settings import *
import os

STATIC_ROOT = '/home/ubuntu/Gaud-E/staticfiles'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'static')

DEBUG=False

REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

SECRET_KEY=os.environ["SECRET_KEY"]

ALLOWED_HOSTS = ['*']
USE_X_FORWARDED_HOST=True
USE_X_FORWARDED_PORT=True

INSTALLED_APPS += ('corsheaders',)
MIDDLEWARE += ('corsheaders.middleware.CorsMiddleware',)
CORS_ORIGIN_ALLOW_ALL = True

SECURE_CROSS_ORIGIN_OPENER_POLICY = None
