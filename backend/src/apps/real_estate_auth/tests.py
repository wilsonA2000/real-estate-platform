from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            name='Test User',
            profile_type='arrendador'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(self.user.profile_type, 'arrendador')
        self.assertTrue(self.user.is_arrendador)
        self.assertFalse(self.user.is_arrendatario)

    def test_user_str_representation(self):
        self.assertEqual(str(self.user), 'Test User (Arrendador)')

class AuthViewsTest(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        
        self.user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
            'name': 'New User',
            'profile_type': 'arrendatario'
        }
        
        self.user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='existingpassword',
            name='Existing User',
            profile_type='arrendador'
        )

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_register_view_post(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(User.objects.count(), 2)
        new_user = User.objects.get(username='newuser')
        self.assertEqual(new_user.email, 'newuser@example.com')
        self.assertEqual(new_user.profile_type, 'arrendatario')

    def test_login_view(self):
        response = self.client.post(self.login_url, {
            'username': 'existinguser',
            'password': 'existingpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirección después del login exitoso