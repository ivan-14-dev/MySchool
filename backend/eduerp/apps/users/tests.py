# backend/apps/users/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from apps.core.models import School
from .models import StudentProfile, TeacherProfile, ParentProfile

User = get_user_model()

class UserTests(APITestCase):
    def setUp(self):
        self.school = School.objects.create(
            name="Test School",
            address="123 Test St",
            city="Test City",
            )

        self.admin_user = User.objects.create_superuser(
            email='admin@eduerp.com',
            password='testpass123',
            first_name='Admin',
            last_name='User'
        )
        self.teacher_user = User.objects.create_user(
            email='teacher@eduerp.com',
            password='testpass123',
            first_name='Teacher',
            last_name='User',
            user_type='teacher'
        )
        self.student_user = User.objects.create_user(
            email='student@eduerp.com',
            password='testpass123',
            first_name='Student',
            last_name='User',
            user_type='student'
        )
        self.client = APIClient()

    def test_create_user(self):
        """Test creating a user"""
        url = reverse('user-list')
        data = {
            'email': 'test@eduerp.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'user_type': 'student'
        }
        
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)
        self.assertEqual(User.objects.get(email='test@eduerp.com').first_name, 'Test')

    def test_retrieve_user(self):
        """Test retrieving a user"""
        url = reverse('user-detail', args=[self.student_user.id])
        
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.student_user.email)

    def test_user_cannot_access_other_users(self):
        """Test that a user cannot access other users' data"""
        url = reverse('user-detail', args=[self.admin_user.id])
        
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)