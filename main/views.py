from django.contrib.auth.decorators import login_required  # to allow only authenticated user to access some views
from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import ToDoList, Item


# Create your views here.


@login_required
def index(request, id):
    # gets a todolist from the database by id
    list = ToDoList.objects.get(id=id)

    # checks if the fetched list belongs to the logged-in user
    if list in request.user.todolist.all():
        # if the request is POST
        if request.method == "POST":
            # if the save button was pressed
            if request.POST.get("save"):
                # loops through all of the items in the list 
                for list_item in list.item_set.all():
                    # if checkbox was clicked, marks it as complete in the database
                    if request.POST.get(f"c{list_item.id}") == "clicked":
                        list_item.complete = True
                    # otherwise marks it as incomplete
                    else:
                        list_item.complete = False
                    # saves the changes
                    list_item.save()
            # else if the newItem button was pressed
            elif request.POST.get("newItem"):
                # gets the text input 
                txt = request.POST.get("new")
                # cif the length of the text the user types is >2, creates a new item
                if len(txt) > 2:
                    list.item_set.create(text=txt, complete=False)
                else:
                    print("invalid")
            # if the delete button was clicked
            elif request.POST.get("delete"):
                # gets the id of the item to delete
                id_to_delete = request.POST.get('delete')
                # gets the item to delete from the database by id
                item_to_delete = Item.objects.get(id=id_to_delete)
                # deletes the item from the database
                item_to_delete.delete()
        # returns the list template
        return render(request, "main/list.html", {"ls": list})
    # if the list does not belong to the user, returns a 404
    return HttpResponseNotFound()


def home(request):
    return render(request, "main/home.html", {})


# @login_required
# def create(response):
#     if response.method == "POST":
#         form = CreateNewList(response.POST)
#         if form.is_valid():
#             n = form.cleaned_data["name"]
#             t = ToDoList(name=n)
#             t.save()
#             response.user.todolist.add(t)

#         return HttpResponseRedirect(f"/{t.id}")
#     else: 
#         form = CreateNewList()
#     return render(response, "main/create.html", {"form":form})   

@login_required
def create(request):
    ls = ToDoList.objects.all()

    if request.method == "POST":
        if request.POST.get("newList"):
            txt = request.POST.get("new")
            if len(txt) > 2:
                t = ToDoList(name=txt)
                t.save()
                request.user.todolist.add(t)
                return render(request, "main/view.html", {})
            else:
                print("invalid")

    return render(request, "main/create.html", {})


@login_required
def view(request):
    ids_to_delete = request.POST.getlist('delete')
    lists_to_delete = ToDoList.objects.filter(id__in=ids_to_delete)
    for list in lists_to_delete:
        list.delete()

    return render(request, "main/view.html", {})
