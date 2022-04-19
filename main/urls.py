from django.urls import path
from main import views

urlpatterns = [
    path("<str:id>", views.index, name = "index"),
    path("", views.home, name = "home"),
    path("create/", views.create, name = "create"),

]