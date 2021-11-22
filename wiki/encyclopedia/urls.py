from django.urls import path

from . import views

#app_name = "tasks"
app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("create", views.create, name="create")
]
