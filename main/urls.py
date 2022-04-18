from django.urls import path
from main import views

urlpatterns = [
    path("<str:name>", views.index, name = "index"),
]