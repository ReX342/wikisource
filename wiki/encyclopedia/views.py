from django import forms
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, reverse
#from django.urls import reverse (already NoReverseMatch without import??!)
from django.contrib import messages
# https://learndjango.com/tutorials/django-markdown-tutorial
from django.views.generic import ListView

from .models import Entry

# https://github.com/sir-ragna/django-wiki
import markdown
from . import util

class BlogListView(ListView):
    model = Entry
    template_name = 'entry_list.html'

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
        # Textarea (from styles.css)
        widget=forms.Textarea(
            attrs={
                # rows for sizing
                'rows': '10',
                # Under (from layout.html) main col-lg-10 col-md-9
                # 'form-control col-md-8 col-lg-8'
                # my-3 is padding: Margin y-axis level 3 (distance between inputfields)
                'class': 'form-control my-3 col-md-10 col-lg-9',
            }
            )   
        )
    #HiddenInput on the widget
    edit = forms.BooleanField(initial=True, widget=forms.HiddenInput())
    
 


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
            # title = title didn't work, so 'edit' for now
            title = form.cleaned_data["title"]
            #request.session["entries"] += [title]
            content = form.cleaned_data["content"]
            #request.session["contents"] += [content]
            if util.get_entry(title) is None: 
            #    pass
                util.save_entry(title,content)
            # https://docs.djangoproject.com/en/3.2/ref/urlresolvers/
                return HttpResponseRedirect(reverse("encyclopedia:index"))
            else:
                check_entry(request, title)                            
                # https://github.com/ReX342/wiki/blob/main/encyclopedia/views.py\
                # Come up with correct use of kwargs
                # https://docs.djangoproject.com/en/3.2/ref/urlresolvers/
                # for considering to reverse to create(.html/path)
                # https://docs.djangoproject.com/en/3.2/topics/http/urls/#topics-http-reversing-url-namespaces
                # for encyclopedia:create             
                # return HttpResponseRedirect(reverse("encyclopedia:create", kwargs={"title": title})) 
                # https://github.com/sir-ragna/django-wiki/blob/main/posts/views.py
                return redirect("encyclopedia:view", kwargs={"title": title}) 
            
    else:
        form = CreateEntry()              
    return render(request, "encyclopedia/create.html", {
        "form": form
    })
    
#get_messages(request)

#We're called on because there's already an entry (with 'title')    
def check_entry(request, title):
    # https://pytutorial.com/django-httpresponse#2
    # return HttpResponse('<h3>We already have that entry!</h3>')    
    
    # lock the editing 
    edit = False
    # and send {title} to create.html so it alerts user
    messages.warning(request, f'We already have an entry for {{ title }}!')
    # https://pythonprogramming.net/messages-django-tutorial/
    form = CreateEntry(request.POST)
    # for msg in form.error_messages:
    #     messages.error(request, f"{msg}: {form.error_messages[msg]}")

                
    
    # https://www.fullstackpython.com/django-forms-booleanfield-examples.html
    #raise forms.ValidationError('We already have an entry by that name!')

    # https://pythonprogramming.net/messages-django-tutorial/
    # https://docs.djangoproject.com/en/3.2/ref/contrib/messages/



    # messages.add_message(request, messages.WARNING, 'We already have an entry by that name!')
    messages.warning(request, 'We already have an entry by that name!')

    #'messages': messages.get_messages(request)
# https://github.com/sir-ragna/django-wiki/blob/main/posts/views.py
def view_entry(request, title):
    if not title in util.list_entries():
        return HttpResponseNotFound("Could not find anything under that entry")
    post_content = util.get_entry(title)
    html_content = markdown.markdown(post_content)
    return render(request, "view_entry", {
        'title': title, 
        'content': html_content
    })    