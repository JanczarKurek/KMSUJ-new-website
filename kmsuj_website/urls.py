"""kmsuj_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name='index'),
    path('<str:name>/', views.page_view, name='page'),
    path('page/addPage/', views.page_edit_view, name='page_add'),
    path('page/<str:name>/edit/', views.page_edit_view, name='page_edit'),
    path('page/<str:name>/delete/', views.page_delete_view, name='page_delete'),
    path(r'^tinymce/', include('tinymce.urls')),
]