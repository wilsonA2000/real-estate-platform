from django.urls import path
from . import views

urlpatterns = [
    path("", views.ratings, name="ratings"),
    path("approve/", views.approve_ratings, name="approve_ratings"),
]
