"""typeidea URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, re_path, path

from blog.views import post_list, post_detail
from config.views import links
from .custom_site import custom_site

urlpatterns = [
    # url(r'^$', post_list),
    # url(r'^category/(?P<category_id>\d+)$', post_list),
    # url(r'^tag/(?P<tag_id>\d+)$', post_list),
    # url(r'^post/(?P<post_id>\d+)$', post_detail),
    # url(r'^links/$', links),
    # # re_path(r'^super_admin/', admin.site.urls),
    # # re_path(r'^admin/', include(custom_site.urls)),
    # url(r'^super_admin/', admin.site.urls),
    # url(r'^admin/', custom_site.urls),

    path('', post_list, name='post_list'),
    path('category/<int:category_id>/', post_list, name='category_post_list'),
    path('tag/<int:tag_id>/', post_list, name='tag_post_list'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('links/', links, name='links'),

    path('super_admin/', admin.site.urls),
    path('admin/', custom_site.urls),
]
