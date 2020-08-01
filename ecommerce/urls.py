"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




# Deployの仕方

# DEBUG=Falseにする

#gitignore作成

# Create a Procfile containing:
# web: gunicorn mysite-project.wsgi --log-file -
# pipenv install gunicorn
# pipenv install psycopg2
# pip install dj-database-url gunicorn whitenoise


# PIPFileかrequirements.txtのどちらか一つで良い
# pipenv run pip freeze > requirements.txt

# pipenv install django_heroku
#import django_heroku
#django_heroku.settings(locals())

# STATIC_ROOT を設定
# python manage.py collectstatic


# ALLOWED_HOSTS = ['django-project7.herokuapp.com/']