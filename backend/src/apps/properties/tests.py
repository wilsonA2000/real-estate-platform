from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Property, PropertyPhoto

User = get_user_model()

class PropertyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            name='Test User',
            profile_type='arrendador'
        )
        
        self.property = Property.objects.create(
            title='Casa de prueba',
            description='Una descripción de prueba',
            location='Bogotá',
            price=1000000,
            property_type='casa',
            owner=self.user
        )

    def test_property_creation(self):
        self.assertEqual(self.property.title, 'Casa de prueba')
        self.assertEqual(self.property.owner, self.user)
        self.assertEqual(self.property.property_type, 'casa')
        self.assertTrue(self.property.is_active)

    def test_property_str_representation(self):
        self.assertEqual(str(self.property), 'Casa de prueba')

class PropertyViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            name='Test User',
            profile_type='arrendador'
        )
        
        self.property = Property.objects.create(
            title='Casa de prueba',
            description='Una descripción de prueba',
            location='Bogotá',
            price=1000000,
            property_type='casa',
            owner=self.user
        )
        
    def test_property_list_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('property_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Casa de prueba')
        
    def test_property_detail_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('property_detail', args=[self.property.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Casa de prueba')
        self.assertContains(response, 'Una descripción de prueba')