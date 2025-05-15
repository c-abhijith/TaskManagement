# core/urls.py
from django.urls import path
from ..views import HelloAPIView, show_hello

urlpatterns = [
    path('api/hello/', HelloAPIView.as_view(), name='hello-api'),
    path('hello-template/', show_hello, name='hello-template'),
]
