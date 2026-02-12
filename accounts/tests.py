from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from snippets.models import Snippet

class SnippetAPITests(APITestCase):
    """Test suite for the Snippet API endpoints"""

    def setUp(self):
        """Create test user and a sample snippet"""
        # Create two users
        self.user1 = User.objects.create_user(username='alice', password='alicepass')
        self.user2 = User.objects.create_user(username='bob', password='bobpass')
        
        # Create a snippet owned by user1
        self.snippet = Snippet.objects.create(
            title='Alice\'s snippet',
            code='print("hello alice")',
            owner=self.user1
        )
        
        # URL endpoints
        self.list_url = reverse('snippet-list')
        self.detail_url = reverse('snippet-detail', args=[self.snippet.id])

    # ------------------------------------------------------------------
    # Unauthenticated access tests
    # ------------------------------------------------------------------
    def test_unauthenticated_can_list_snippets(self):
        """GET /api/snippets/ should be public"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_can_retrieve_snippet(self):
        """GET /api/snippets/<pk>/ should be public"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.snippet.title)

    def test_unauthenticated_cannot_create_snippet(self):
        """POST /api/snippets/ should require authentication"""
        response = self.client.post(self.list_url, {
            'title': 'Hack',
            'code': 'print("evil")'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # or 401 if you change settings

    def test_unauthenticated_cannot_update_snippet(self):
        """PUT /api/snippets/<pk>/ should require authentication"""
        response = self.client.put(self.detail_url, {
            'title': 'Hacked title',
            'code': self.snippet.code
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_delete_snippet(self):
        """DELETE /api/snippets/<pk>/ should require authentication"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ------------------------------------------------------------------
    # Authenticated access tests (as user1)
    # ------------------------------------------------------------------
    def test_authenticated_can_create_snippet(self):
        """POST /api/snippets/ with authentication should succeed"""
        self.client.login(username='alice', password='alicepass')
        response = self.client.post(self.list_url, {
            'title': 'New snippet',
            'code': 'x = 42'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Snippet.objects.count(), 2)
        self.assertEqual(response.data['owner'], self.user1.id)

    def test_owner_can_update_snippet(self):
        """PUT /api/snippets/<pk>/ as owner should succeed"""
        self.client.login(username='alice', password='alicepass')
        response = self.client.put(self.detail_url, {
            'title': 'Updated title',
            'code': self.snippet.code
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.snippet.refresh_from_db()
        self.assertEqual(self.snippet.title, 'Updated title')

    def test_owner_can_delete_snippet(self):
        """DELETE /api/snippets/<pk>/ as owner should succeed"""
        self.client.login(username='alice', password='alicepass')
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Snippet.objects.filter(id=self.snippet.id).exists())

    # ------------------------------------------------------------------
    # Permission tests: non-owner (user2) cannot modify
    # ------------------------------------------------------------------
    def test_non_owner_cannot_update_snippet(self):
        """PUT /api/snippets/<pk>/ as non-owner should be forbidden"""
        self.client.login(username='bob', password='bobpass')
        response = self.client.put(self.detail_url, {
            'title': 'Bob wants to hack',
            'code': self.snippet.code
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_owner_cannot_delete_snippet(self):
        """DELETE /api/snippets/<pk>/ as non-owner should be forbidden"""
        self.client.login(username='bob', password='bobpass')
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ------------------------------------------------------------------
    # Authentication method tests
    # ------------------------------------------------------------------
    def test_login_required_for_write_actions(self):
        """Ensure login is required for POST/PUT/DELETE"""
        # Try to create without logging in
        response = self.client.post(self.list_url, {
            'title': 'No auth',
            'code': 'fail'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Now login and try again
        self.client.login(username='alice', password='alicepass')
        response = self.client.post(self.list_url, {
            'title': 'With auth',
            'code': 'win'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
