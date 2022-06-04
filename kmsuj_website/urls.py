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
from django.urls import path, include, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name='index'),
    path('ossm/', views.ossm_index_view, name='ossm_index'),
    re_path(r'^workshop/(?P<lang>[a-z]{2})/$', views.workshop_index_view, name='workshop_index'),
    path('workshop/', views.workshop_index_view, name='workshop_index'),
    path('<slug:name>/', views.page_view,name='page'),
    path('page/addPage/', views.page_edit_view, name='page_add'),
    path('page/<slug:name>/edit/', views.page_edit_view, name='page_edit'),
    path('page/<slug:name>/delete/', views.page_delete_view,name='page_delete'),
    path('ossm/<slug:name>/', views.ossm_page_view, name='ossm_page'),
    path('ossm/page/addPage/', views.ossm_page_edit_view, name='ossm_page_add'),
    path('ossm/page/<slug:name>/edit/', views.ossm_page_edit_view,  name='ossm_page_edit'),
    path('ossm/page/<slug:name>/delete/', views.ossm_page_delete_view, name='ossm_page_delete'),
    path('workshop/<slug:name>/<str:lang>', views.workshop_page_view, name='workshop_page'),
    path('workshop/<slug:name>/', views.workshop_page_view, name='workshop_page'),
    path('workshop/page/addPage/', views.workshop_page_edit_view, name='workshop_page_add'),
    path('workshop/page/<slug:name>/edit/<str:lang>', views.workshop_page_edit_view,  name='workshop_page_edit'),
    path('workshop/page/<slug:name>/delete/<str:lang>', views.workshop_page_delete_view, name='workshop_page_delete'),
    re_path(r'^tinymce/', include('tinymce.urls')),
]