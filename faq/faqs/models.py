from django.db import models
from ckeditor.fields import RichTextField
from django.core.cache import cache
from .utils.translator import translate_text

LANGUAGE_CHOICES = [
    ('en', 'English'),
    ('hi', 'Hindi'),
    ('bn', 'Bengali'),
]

class FAQ(models.Model):
    # Base fields (English version)
    question = models.TextField()
    answer = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Translated fields
    question_hi = models.TextField(blank=True)
    answer_hi = RichTextField(blank=True)
    question_bn = models.TextField(blank=True)
    answer_bn = RichTextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.question[:50]
    
    def get_translated_field(self, field_name, lang):
        """Get translated version of a field"""
        if lang == 'en':
            return getattr(self, field_name)
            
        cache_key = f'faq_{self.id}_{field_name}_{lang}'
        cached_value = cache.get(cache_key)
            
        if cached_value:
            return cached_value
        
        translated_field = getattr(self, f'{field_name}_{lang}')
        if not translated_field:
            # Translate and cache if translation doesn't exist
            original_text = getattr(self, field_name)
            translated_field = translate_text(original_text, lang)
            setattr(self, f'{field_name}_{lang}', translated_field)
            self.save(update_fields=[f'{field_name}_{lang}'])
            cache.set(cache_key, translated_field, timeout=86400)  # Cache for 24 hours
        
        return translated_field
    
    def save(self, *args, **kwargs):
        """Override save to handle translations"""
        is_new = self.pk is None
        
        # First save to ensure we have a primary key
        super().save(*args, **kwargs)
        
        # Only translate on creation and when not doing an update_fields save
        if is_new and not kwargs.get('update_fields'):
            # Translate to all supported languages on creation
            for lang_code, _ in LANGUAGE_CHOICES:
                if lang_code != 'en':
                    # Use the language code from the loop
                    setattr(self, f'question_{lang_code}', 
                           translate_text(self.question, lang_code))
                    setattr(self, f'answer_{lang_code}', 
                           translate_text(self.answer, lang_code))
            
            # Save again with the translations
            super().save(update_fields=[
                'question_hi', 'answer_hi',
                'question_bn', 'answer_bn'
            ])