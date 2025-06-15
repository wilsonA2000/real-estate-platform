from rest_framework import serializers
from .models import Property, PropertyPhoto

class PropertyPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyPhoto
        fields = ['id', 'image', 'uploaded_at']

class PropertySerializer(serializers.ModelSerializer):
    related_photos = PropertyPhotoSerializer(many=True, read_only=True)
    owner_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = [
            'id', 'title', 'description', 'location', 'exact_address',
            'price', 'currency', 'property_type', 'video', 'video_url',
            'requirements', 'characteristics', 'owner', 'owner_name',
            'created_at', 'is_active', 'bedrooms', 'bathrooms',
            'parking_spaces', 'construction_area', 'land_area',
            'main_photo', 'related_photos', 'latitude', 'longitude'
        ]
        read_only_fields = ['owner', 'created_at']
    
    def get_owner_name(self, obj):
        return obj.owner.name if obj.owner else None

class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'location', 'exact_address',
            'price', 'currency', 'property_type', 'video', 'video_url',
            'requirements', 'characteristics', 'bedrooms', 'bathrooms',
            'parking_spaces', 'construction_area', 'land_area',
            'main_photo', 'latitude', 'longitude'
        ]
    
    def create(self, validated_data):
        user = self.context['request'].user
        property_obj = Property.objects.create(owner=user, **validated_data)
        return property_obj