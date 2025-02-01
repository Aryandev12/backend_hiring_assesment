# faqs/tests/conftest.py
import pytest
from django.core.cache import cache

@pytest.fixture(autouse=True)
def clean_cache():
    cache.clear()
    yield
    cache.clear()

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()