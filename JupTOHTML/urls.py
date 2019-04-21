from django.conf.urls import url
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.urls import path

from . import views


urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^download/$', views.download),
]

