from rest_framework import serializers
from .models import FAQ

class FAQSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()
    question_en = serializers.CharField(write_only=True, source='question')
    answer_en = serializers.CharField(write_only=True, source='answer')

    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'created_at', 'updated_at', 'question_en', 'answer_en']

    def get_question(self, obj):
        lang = self.context.get('lang', 'en')
        return obj.get_translated_field('question', lang)

    def get_answer(self, obj):
        lang = self.context.get('lang', 'en')
        return obj.get_translated_field('answer', lang)