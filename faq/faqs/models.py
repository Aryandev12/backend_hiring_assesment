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
            self.save()
            cache.set(cache_key, translated_field, timeout=86400)  # Cache for 24 hours

        return translated_field

    def save(self, *args, **kwargs):
        """Override save to handle translations"""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            # Translate to all supported languages on creation
            for lang_code, _ in LANGUAGE_CHOICES:
                if lang_code != 'en':
                    self.question_hi = translate_text(self.question, 'hi')
                    self.answer_hi = translate_text(self.answer, 'hi')
                    self.question_bn = translate_text(self.question, 'bn')
                    self.answer_bn = translate_text(self.answer, 'bn')
            super().save(*args, **kwargs)
