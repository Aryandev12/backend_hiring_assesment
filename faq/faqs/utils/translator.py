from googletrans import Translator

def translate_text(text, target_lang):
    """
    Translate text to target language using Google Translate
    """
    try:
        translator = Translator()
        translation = translator.translate(text, dest=target_lang)
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Fallback to original text