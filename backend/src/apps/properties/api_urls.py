from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import PropertyViewSet, PropertyPhotoViewSet

router = DefaultRouter()
router.register(r'properties', PropertyViewSet)
router.register(r'property-photos', PropertyPhotoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]