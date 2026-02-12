from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from snippets.models import Snippet

class SnippetAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='alice', password='alicepass')
        self.user2 = User.objects.create_user(username='bob', password='bobpass')
        self.snippet = Snippet.objects.create(
            title='Alice\'s snippet',
            code='print("hello alice")',
            owner=self.user1
        )
        self.list_url = reverse('snippet-list')
        self.detail_url = reverse('snippet-detail', args=[self.snippet.id])

    # Unauthenticated tests
    def test_unauthenticated_can_list_snippets(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_can_retrieve_snippet(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_cannot_create_snippet(self):
        response = self.client.post(self.list_url, {'title': 'Hack', 'code': 'print'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_update_snippet(self):
        response = self.client.put(self.detail_url, {'title': 'Hack', 'code': 'print'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_delete_snippet(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Authenticated as owner
    def test_authenticated_can_create_snippet(self):
        self.client.login(username='alice', password='alicepass')
        response = self.client.post(self.list_url, {'title': 'New', 'code': 'x=42'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_owner_can_update_snippet(self):
        self.client.login(username='alice', password='alicepass')
        response = self.client.put(self.detail_url, {'title': 'Updated', 'code': self.snippet.code}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_can_delete_snippet(self):
        self.client.login(username='alice', password='alicepass')
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Non-owner tests
    def test_non_owner_cannot_update_snippet(self):
        self.client.login(username='bob', password='bobpass')
        response = self.client.put(self.detail_url, {'title': 'Hack', 'code': self.snippet.code}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_owner_cannot_delete_snippet(self):
        self.client.login(username='bob', password='bobpass')
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Login required
    def test_login_required_for_write_actions(self):
        response = self.client.post(self.list_url, {'title': 'No auth'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.login(username='alice', password='alicepass')
        response = self.client.post(self.list_url, {'title': 'With auth', 'code': 'win'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)# Create your tests here.
