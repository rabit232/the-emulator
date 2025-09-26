#!/usr/bin/env python3
"""
Basic Usage Example for The Emulator

This example demonstrates the core functionality of the Advanced LLM Emulator,
including emotional intelligence, knowledge management, and multi-language support.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from emulator import AdvancedLLMEmulator


def main():
    """Demonstrate basic emulator functionality."""
    
    print("🤖 The Emulator - Basic Usage Example")
    print("=" * 50)
    
    # Initialize the emulator
    print("\n1. Initializing Advanced LLM Emulator...")
    emulator = AdvancedLLMEmulator(personality="curious_researcher")
    
    # Get personality information
    personality_info = emulator.get_personality_info()
    print(f"   Personality: {personality_info['personality']}")
    print(f"   Session ID: {personality_info['session_id']}")
    
    # Test basic conversation
    print("\n2. Testing Basic Conversation...")
    questions = [
        "Hello! Can you introduce yourself?",
        "What are your main capabilities?",
        "Explain quantum computing in simple terms",
        "How do you handle emotions in conversations?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n   Q{i}: {question}")
        response = emulator.get_decision(question)
        print(f"   A{i}: {response}")
    
    # Test knowledge management
    print("\n3. Testing Knowledge Management...")
    
    # Store some knowledge
    emulator.store_knowledge("favorite_color", "quantum blue")
    emulator.store_knowledge("programming_languages", ["Python", "JavaScript", "Rust"])
    emulator.store_knowledge("creation_date", "2025-09-26")
    
    # Retrieve knowledge
    color = emulator.retrieve_knowledge("favorite_color")
    languages = emulator.retrieve_knowledge("programming_languages")
    
    print(f"   Stored favorite color: {color}")
    print(f"   Stored languages: {languages}")
    
    # Test emotional analysis
    print("\n4. Testing Emotional Analysis...")
    test_texts = [
        "I'm so excited about this new project!",
        "I'm feeling a bit confused about this concept.",
        "This is absolutely fascinating and wonderful!",
        "I'm worried about the deadline approaching."
    ]
    
    for text in test_texts:
        emotion_analysis = emulator.analyze_emotion(text)
        print(f"   Text: '{text}'")
        print(f"   Detected emotion: {emotion_analysis}")
    
    # Test capabilities
    print("\n5. Checking System Capabilities...")
    capabilities = emulator.get_capabilities()
    for capability, enabled in capabilities.items():
        status = "✅ Enabled" if enabled else "❌ Disabled"
        print(f"   {capability}: {status}")
    
    # Get session statistics
    print("\n6. Session Statistics...")
    stats = emulator.get_session_stats()
    print(f"   Interactions: {stats['interactions_count']}")
    print(f"   Knowledge entries: {stats['knowledge_entries']}")
    print(f"   Current emotional state: {stats['current_emotion']}")
    
    print("\n🎉 Basic usage demonstration complete!")
    print("\nThe Emulator is ready for advanced AI emulation tasks.")


if __name__ == "__main__":
    main()
