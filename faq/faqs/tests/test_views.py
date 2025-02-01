# faqs/tests/test_views.py
import pytest
from rest_framework import status
from django.urls import reverse
from faqs.models import FAQ

@pytest.mark.django_db
class TestFAQViewSet:
    @pytest.fixture(autouse=True)
    def setup_method(self, db):
        self.faqs = []
        for i in range(3):
            faq = FAQ.objects.create(
                question=f"Question {i}",
                answer=f"Answer {i}"
            )
            self.faqs.append(faq)
    
    def test_list_faqs(self, api_client):
        url = reverse('faq-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3
        
    def test_retrieve_faq(self, api_client):
        url = reverse('faq-detail', kwargs={'pk': self.faqs[0].pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['question'] == "Question 0"
        
    def test_language_parameter(self, api_client):
        url = reverse('faq-list')
        response = api_client.get(f"{url}?lang=hi")
        
        assert response.status_code == status.HTTP_200_OK
        # Check if translation is different from original
        assert response.data['results'][0]['question'] != "Question 0"
        
    def test_caching(self, api_client):
        url = reverse('faq-list')
        
        # First request
        response1 = api_client.get(url)
        assert response1.status_code == status.HTTP_200_OK
        
        # Second request should be cached
        response2 = api_client.get(url)
        assert response2.status_code == status.HTTP_200_OK
        assert response2.data == response1.data