from django.urls import path
from main import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("v1/", views.v1, name = "view 1"),
]