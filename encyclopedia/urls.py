from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("search", views.search, name="search"),  
    path("new_entry", views.new_entry, name="new_entry"),
    path("random_entry", views.random_entry, name="random_entry"),
]
