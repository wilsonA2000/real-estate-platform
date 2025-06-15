from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.PropertyListView.as_view(), name="property_list"),
    path("<int:pk>/", views.PropertyDetailView.as_view(), name="property_detail"),
    path("create/", views.PropertyCreateView.as_view(), name="property_create"),
    path("<int:pk>/edit/", views.PropertyUpdateView.as_view(), name="property_edit"),
    path("<int:pk>/delete/", views.PropertyDeleteView.as_view(), name="property_delete"),
]