from django.contrib import admin
from .models import ContactRequest

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'property', 'owner', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('tenant__username', 'tenant__name', 'owner__username', 'owner__name', 'property__title', 'message')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    
    fieldsets = (
        (None, {
            'fields': ('tenant', 'owner', 'property')
        }),
        ('Mensaje', {
            'fields': ('message', 'email', 'phone')
        }),
        ('Estado', {
            'fields': ('is_read', 'created_at')
        }),
    )