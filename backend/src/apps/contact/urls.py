from django.urls import path
from . import views

urlpatterns = [
    path('requests/', views.contact_requests, name='contact_requests'),
    path('requests/<int:request_id>/process/', views.process_contact_request, name='process_contact_request'),
    path('tenant/<int:tenant_id>/', views.view_tenant_profile, name='view_tenant_profile'),
    path('tenant/<int:tenant_id>/request/<int:request_id>/', views.view_tenant_profile, name='view_tenant_profile_with_request'),
]