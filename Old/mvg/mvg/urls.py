from django.contrib import admin
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls,name="admin"),
    url(r'^portfolio/',include(('portfolio.urls',"portfolio"),namespace="portfolio")),
    url(r'^$', views.homepage, name="home"),
]
