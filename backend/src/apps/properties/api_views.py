from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Property, PropertyPhoto
from .serializers import PropertySerializer, PropertyCreateSerializer, PropertyPhotoSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a los propietarios de un objeto editarlo.
    """
    def has_object_permission(self, request, view, obj):
        # Permisos de lectura permitidos para cualquier solicitud
        if request.method in permissions.SAFE_METHODS:
            return True
        # Permisos de escritura solo para el propietario
        return obj.owner == request.user

class PropertyViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver y editar propiedades.
    """
    queryset = Property.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['property_type', 'location', 'is_active']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['price', 'created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PropertyCreateSerializer
        return PropertySerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    @extend_schema(
        parameters=[
            OpenApiParameter(name='min_price', description='Precio mínimo', required=False, type=float),
            OpenApiParameter(name='max_price', description='Precio máximo', required=False, type=float),
            OpenApiParameter(name='bedrooms', description='Número de habitaciones', required=False, type=int),
            OpenApiParameter(name='bathrooms', description='Número de baños', required=False, type=int),
        ]
    )
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Búsqueda avanzada de propiedades con filtros adicionales.
        """
        queryset = self.get_queryset()
        
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        bedrooms = request.query_params.get('bedrooms')
        bathrooms = request.query_params.get('bathrooms')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if bedrooms:
            queryset = queryset.filter(bedrooms=bedrooms)
        if bathrooms:
            queryset = queryset.filter(bathrooms=bathrooms)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class PropertyPhotoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar fotos de propiedades.
    """
    queryset = PropertyPhoto.objects.all()
    serializer_class = PropertyPhotoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        property_id = self.request.data.get('property')
        property_obj = Property.objects.get(id=property_id)
        
        # Verificar que el usuario es el propietario
        if property_obj.owner != self.request.user:
            self.permission_denied(self.request, message="No tienes permiso para añadir fotos a esta propiedad.")
        
        serializer.save()