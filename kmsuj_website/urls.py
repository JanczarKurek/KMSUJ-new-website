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
    path('ossm/', views.ossm_index_view, name='ossm_index'),
    path('warsztaty/', views.warsztaty_index_view, name='warsztaty_index'),
    path('<str:name>/', views.page_view,name='page'),
    path('page/addPage/', views.page_edit_view, name='page_add'),
    path('page/<str:name>/edit/', views.page_edit_view, name='page_edit'),
    path('page/<str:name>/delete/', views.page_delete_view,name='page_delete'),
    path('ossm/<str:name>/', views.ossm_page_view, name='ossm_page'),
    path('ossm/page/addPage/', views.ossm_page_edit_view, name='ossm_page_add'),
    path('ossm/page/<str:name>/edit/', views.ossm_page_edit_view,  name='ossm_page_edit'),
    path('ossm/page/<str:name>/delete/', views.ossm_page_delete_view, name='ossm_page_delete'),
    path('warsztaty/<str:name>/', views.warsztaty_page_view, name='warsztaty_page'),
    path('warsztaty/page/addPage/', views.warsztaty_page_edit_view, name='warsztaty_page_add'),
    path('warsztaty/page/<str:name>/edit/', views.warsztaty_page_edit_view,  name='warsztaty_page_edit'),
    path('warsztaty/page/<str:name>/delete/', views.warsztaty_page_delete_view, name='warsztaty_page_delete'),
    path(r'^tinymce/', include('tinymce.urls')),
]