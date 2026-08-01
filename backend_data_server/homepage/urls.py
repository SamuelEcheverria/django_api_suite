from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="homepage"),
    path("index/", views.index, name="index"),
]