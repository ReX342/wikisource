from django.urls import path

from . import views
from .views import BlogListView

#app_name = "tasks"
app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("create", views.create, name="create"),
    path("<str:title>", views.view_entry, name="title"),
    #path('', BlogListView... oldcode)
    #path('blog', BlogListView.as_view(), name='entry_list'),
]
