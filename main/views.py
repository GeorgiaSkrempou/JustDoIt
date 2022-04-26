from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList
from django.contrib.auth.decorators import login_required # to allow only authenticated user to access some views
# Create your views here.




@login_required
def index(request, id):
    ls = ToDoList.objects.get(id=id)

    if ls in request.user.todolist.all():
        if request.method == "POST":
            #print(response.POST)
            if request.POST.get("save"):
                for item in ():
                    if request.POST.get("c" + str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    item.save()
            elif request.POST.get("newItem"):
                txt = request.POST.get("new")
                if len(txt) > 2:
                    ls.item_set.create(text=txt, complete = False)
                else:
                    print("invalid")

            elif request.POST.get("delete"):
                for item in ls.item_set.all():
                    if request.POST.get(f"c{item.id}") == "clicked":
                        item.delete()


        return render(request, "main/list.html", {"ls":ls})

    return render(request, "main/view.html", {})
    
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
                t=ToDoList(name=txt)
                t.save()
                request.user.todolist.add(t)
                return HttpResponseRedirect(f"/{t.id}")
            else:
                print("invalid")
            
    return render(request, "main/create.html", {})




@login_required
def view(request):
    ids_to_delete = request.POST.getlist('clicked')
    to_delete = ToDoList.objects.filter(id__in=ids_to_delete)
    print(to_delete)
    for list in to_delete:
        list.delete()
   
    return  render(request, "main/view.html", {})


