import pytest
from django.core.cache import cache
from rest_framework.test import APIClient
from faqs.models import FAQ

@pytest.mark.django_db
class TestFAQAPI:
    @pytest.fixture(autouse=True)
    def setup_method(self, db):
        self.client = APIClient()
        self.faq = FAQ.objects.create(
            question="How does the refund process work?",
            answer="Refunds are processed within 7-10 business days after approval."
        )
    
    def test_fetch_faqs_in_hindi(self):
        """Ensure FAQs are returned in Hindi when requested."""
        response = self.client.get("/api/faqs/?lang=hi")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        
        faq_data = response.json()[0]
        assert 'question' in faq_data
        assert 'answer' in faq_data
        assert faq_data['question'] != "How does the refund process work?"
        assert faq_data['answer'] != "Refunds are processed within 7-10 business days after approval."
    def test_fetch_faqs_in_english(self):
        """Ensure the default response contains English FAQs."""
        response = self.client.get("/api/faqs/?lang=en")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        faq_data = response.json()[0]
        assert faq_data['question'] == "How does the refund process work?"
        assert faq_data['answer'] == "Refunds are processed within 7-10 business days after approval."
  
    