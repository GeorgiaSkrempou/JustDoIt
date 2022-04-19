from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList
# Create your views here.

def index(response, name):
    ls = ToDoList.objects.get(name=name)
    return render(response, "main/list.html", {"ls":ls})
    
def home(response):
    return render(response, "main/home.html", {})

def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()

        return HttpResponseRedirect(f"/{str(t.name)}")
    else: 
        form = CreateNewList()
    return render(response, "main/create.html", {"form":form})    
