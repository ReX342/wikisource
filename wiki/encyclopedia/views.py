from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import util

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    # priority = forms.IntegerField(label="Priority", min_value=1, max_value=5)

class CreateEntry(forms.Form):
    #title = forms.CharField(label="Title"),
    # Mind the typo on Charfield
    # https://docs.djangoproject.com/en/3.2/ref/forms/widgets/
    # comment = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))
    title = forms.CharField(
    label="Title",
    max_length="111",
    widget=forms.TextInput(attrs={
        'size': '40'
        })
    )    
    #content = forms.Textarea(label="New Entry"),
    content = forms.CharField(
        label="Entry Content",
        # Textarea
        widget=forms.Textarea(
            attrs={
                # rows for sizing
                'size': '10'
            }
            )   
        )
    edit = forms.BooleanField(initial=True)
    
 


def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "encyclopedia/index.html", {
        "tasks": request.session["tasks"],
        "entries": util.list_entries()
    })

# Create your views here.
def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("encyclopedia:index"))
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/add.html", {
            "form": NewTaskForm()
        })

def create(request):
    if request.method == "POST":
        form = CreateEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["edit"]
            #request.session["entries"] += [title]
            content = form.cleaned_data["content"]
            #request.session["contents"] += [content]
            if util.get_entry(title) is not None: 
                pass
            # https://docs.djangoproject.com/en/3.2/ref/urlresolvers/
            #          
            #    util.save_entry(title,content)
            return HttpResponseRedirect(reverse("encyclopedia:index"))
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/create.html", {
            "form": CreateEntry()
        })