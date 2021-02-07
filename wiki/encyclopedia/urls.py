from django.urls import path
from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.entry_page, name="entry"),
    path("new_page/", views.new_page, name="new_page"),
    path("wiki/edit/<str:title>", views.edit_page, name="edit"),
    path("search/", views.search, name="search"),
    path("random", views.random_page, name="random_page")
    
]
    
