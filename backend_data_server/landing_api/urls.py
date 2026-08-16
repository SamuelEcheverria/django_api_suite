from django.urls import path
from . import views

urlpatterns = [
    path("", views.LandingAPI.as_view(), name="landing_api_resources"),
    path("index/", views.LandingAPI.as_view(), name="landing_api_resources_index"),
    path("<str:collection>/", views.LandingAPI.as_view(), name="landing_api_collection"),
]
