# faqs/tests/test_models.py
import pytest
from django.core.cache import cache
from faqs.models import FAQ

@pytest.mark.django_db
class TestFAQModel:
    @pytest.fixture(autouse=True)
    def setup_method(self, db):
        self.faq = FAQ.objects.create(
            question="What is Python?",
            answer="Python is a programming language."
        )
    
    def test_faq_creation(self):
        assert FAQ.objects.count() == 1
        assert self.faq.question == "What is Python?"
        
    def test_str_representation(self):
        assert str(self.faq) == "What is Python?"
        
    def test_auto_translation(self):
        # Check if translations were automatically generated
        assert hasattr(self.faq, 'question_hi')
        assert hasattr(self.faq, 'question_bn')
        
    def test_get_translated_field(self):
        # Test English (default)
        assert self.faq.get_translated_field('question', 'en') == "What is Python?"
        
        # Test Hindi translation
        hindi_translation = self.faq.get_translated_field('question', 'hi')
        assert isinstance(hindi_translation, str)
        assert hindi_translation != "What is Python?"
        
    def test_caching(self):
        # Clear cache first
        cache.clear()
        
        # First call should cache the translation
        translation = self.faq.get_translated_field('question', 'hi')
        cache_key = f'faq_{self.faq.id}_question_hi'
        
        # Check if translation is cached
        assert cache.get(cache_key) == translation