"""Services for the main app."""
import os
import json
from typing import Dict, List, Optional, Any
import logging

import openai
import anthropic
from django.conf import settings

logger = logging.getLogger(__name__)

# Initialize API clients
openai_client = openai.OpenAI(api_key=os.environ.get('OPENAI_API_KEY', ''))
anthropic_client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY', ''))

# Define supported languages
SUPPORTED_LANGUAGES = [
    ("cornish", "Cornish"),
    ("manx", "Manx"),
    ("breton", "Breton"),
    ("inuktitut", "Inuktitut"),
    ("kalaallisut", "Kalaallisut"),
    ("romani", "Romani"),
    ("occitan", "Occitan"),
    ("ladino", "Ladino"),
    ("northern_sami", "Northern Sami"),
    ("upper_sorbian", "Upper Sorbian"),
    ("kashubian", "Kashubian"),
    ("zazaki", "Zazaki"),
    ("chuvash", "Chuvash"),
    ("livonian", "Livonian"),
    ("tsakonian", "Tsakonian"),
    ("saramaccan", "Saramaccan"),
    ("bislama", "Bislama")
]

class TranslationService:
    """Service for translating text using AI models."""
    
    @classmethod
    def translate_with_openai(cls, text: str, target_language: str) -> str:
        """Translate text using OpenAI API."""
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are a professional translator specializing in rare languages. Translate the following text to {target_language}. Keep all formatting and structure intact. Only return the translated text, nothing else."},
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
                max_tokens=4000
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI translation error: {e}")
            return f"Translation error: {e}"
    
    @classmethod
    def translate_with_anthropic(cls, text: str, target_language: str) -> str:
        """Translate text using Anthropic API."""
        try:
            response = anthropic_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=4000,
                temperature=0.3,
                system=f"You are a professional translator specializing in rare languages. Translate the following text to {target_language}. Keep all formatting and structure intact. Only return the translated text, nothing else.",
                messages=[
                    {"role": "user", "content": text}
                ]
            )
            return response.content[0].text.strip()
        except Exception as e:
            logger.error(f"Anthropic translation error: {e}")
            # If Anthropic fails, try OpenAI as a fallback
            try:
                return cls.translate_with_openai(text, target_language)
            except Exception as fallback_error:
                logger.error(f"Fallback to OpenAI also failed: {fallback_error}")
                return f"Translation error: {e}"
    
    @classmethod
    def translate(cls, text: str, target_language: str, service: str = "anthropic") -> str:
        """Translate text using the specified service."""
        if not text or not target_language:
            return text
            
        # Prefer Anthropic if key is available, otherwise use OpenAI
        if service == "anthropic" and os.environ.get('ANTHROPIC_API_KEY'):
            return cls.translate_with_anthropic(text, target_language)
        else:
            return cls.translate_with_openai(text, target_language)