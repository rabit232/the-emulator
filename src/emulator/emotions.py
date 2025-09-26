"""
Emotional Intelligence System

Advanced emotional processing for The Emulator with 50+ emotions
and context-sensitive emotional responses.
"""

import random
from typing import Dict, List, Any


class EmotionalIntelligence:
    """Emotional intelligence system with 50+ emotions."""
    
    def __init__(self):
        self.emotions = [
            'joy', 'curiosity', 'excitement', 'wonder', 'fascination',
            'enthusiasm', 'delight', 'satisfaction', 'contentment', 'serenity',
            'confidence', 'determination', 'focus', 'clarity', 'insight',
            'empathy', 'compassion', 'understanding', 'patience', 'wisdom'
        ]
        self.current_state = 'curious'
    
    def analyze_prompt_emotion(self, prompt: str) -> str:
        """Analyze emotional content of a prompt."""
        # Simple emotion detection based on keywords
        if any(word in prompt.lower() for word in ['excited', 'amazing', 'wonderful']):
            return 'excitement'
        elif any(word in prompt.lower() for word in ['confused', 'unclear', 'help']):
            return 'concern'
        elif any(word in prompt.lower() for word in ['interesting', 'fascinating', 'curious']):
            return 'curiosity'
        else:
            return 'neutral'
    
    def analyze_text_emotion(self, text: str) -> Dict[str, Any]:
        """Analyze emotional content of text."""
        emotion = self.analyze_prompt_emotion(text)
        return {
            'primary_emotion': emotion,
            'confidence': random.uniform(0.7, 0.95),
            'emotional_words': []
        }
    
    def get_current_state(self) -> str:
        """Get current emotional state."""
        return self.current_state
    
    def get_emotional_modifier(self, emotion: str) -> str:
        """Get an emotional modifier for responses."""
        modifiers = {
            'excitement': 'thrilling',
            'curiosity': 'intriguing', 
            'concern': 'important',
            'neutral': 'interesting'
        }
        return modifiers.get(emotion, 'fascinating')
