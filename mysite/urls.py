"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from django.conf import settings
from PilkaNozna import views as myapp_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('PilkaNozna/', include('PilkaNozna.urls')),
    #path('registration/', include('registration.urls')),
    #url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})
]
#handler404 = 'mysite.views.not_found'
#urlpatterns += staticfiles_urlpatterns()

handler404 = myapp_views.error_404
handler500 = myapp_views.error_500