"""
Knowledge Management System

Dynamic knowledge storage and retrieval system for The Emulator
with persistent storage capabilities.
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime


class KnowledgeManager:
    """Knowledge management system with persistent storage."""
    
    def __init__(self, knowledge_file: Optional[str] = None):
        self.knowledge_file = knowledge_file or "emulator_knowledge.json"
        self.knowledge_base = {}
        self.interactions = []
        self._load_knowledge()
    
    def store_knowledge(self, key: str, value: Any) -> bool:
        """Store knowledge in the knowledge base."""
        try:
            self.knowledge_base[key] = {
                'value': value,
                'timestamp': datetime.now().isoformat(),
                'type': type(value).__name__
            }
            self._save_knowledge()
            return True
        except Exception:
            return False
    
    def retrieve_knowledge(self, key: str) -> Any:
        """Retrieve knowledge from the knowledge base."""
        entry = self.knowledge_base.get(key)
        if entry:
            return entry['value']
        return None
    
    def store_interaction(self, prompt: str, response: str, emotion: str) -> None:
        """Store an interaction for learning purposes."""
        interaction = {
            'prompt': prompt,
            'response': response,
            'emotion': emotion,
            'timestamp': datetime.now().isoformat()
        }
        self.interactions.append(interaction)
        
        # Keep only last 100 interactions to prevent memory issues
        if len(self.interactions) > 100:
            self.interactions = self.interactions[-100:]
        
        self._save_knowledge()
    
    def get_interaction_count(self) -> int:
        """Get the number of stored interactions."""
        return len(self.interactions)
    
    def get_knowledge_count(self) -> int:
        """Get the number of knowledge entries."""
        return len(self.knowledge_base)
    
    def _load_knowledge(self) -> None:
        """Load knowledge from persistent storage."""
        if os.path.exists(self.knowledge_file):
            try:
                with open(self.knowledge_file, 'r') as f:
                    data = json.load(f)
                    self.knowledge_base = data.get('knowledge', {})
                    self.interactions = data.get('interactions', [])
            except Exception:
                # If loading fails, start with empty knowledge base
                self.knowledge_base = {}
                self.interactions = []
    
    def _save_knowledge(self) -> None:
        """Save knowledge to persistent storage."""
        try:
            data = {
                'knowledge': self.knowledge_base,
                'interactions': self.interactions,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.knowledge_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception:
            # Silently fail if saving is not possible
            pass
