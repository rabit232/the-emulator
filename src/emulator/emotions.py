#!/usr/bin/env python3
"""
Enhanced Emotional Intelligence System for The Emulator

This module provides sophisticated emotional intelligence with detailed emotion definitions,
contextual triggers, and behavioral patterns for more nuanced AI interactions.

Based on the enhanced_emotions.py from Ribit 2.0 collection.
"""

import random
import json
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class EmotionDefinition:
    """Detailed definition of an emotion with context and behaviors."""
    name: str
    description: str
    intensity_range: Tuple[float, float]  # (min, max) intensity 0.0-1.0
    triggers: List[str]  # Situations that trigger this emotion
    expressions: List[str]  # How this emotion is expressed
    behaviors: List[str]  # Behavioral patterns when experiencing this emotion
    related_emotions: List[str]  # Emotions that often occur together
    duration_typical: int  # Typical duration in seconds
    physical_manifestations: List[str]  # How emotion affects "physical" responses
    cognitive_effects: List[str]  # How emotion affects thinking patterns
    social_context: List[str]  # When this emotion is appropriate socially

class EmotionalIntelligence:
    """
    Enhanced emotional intelligence system with detailed emotion modeling.
    
    Provides sophisticated emotional responses with context awareness,
    intensity modeling, and realistic emotional transitions.
    """
    
    def __init__(self):
        """Initialize the enhanced emotional intelligence system."""
        self.current_emotions = {}  # emotion_name -> intensity
        self.emotion_history = []  # List of (timestamp, emotion, intensity, context)
        self.personality_traits = {
            "wisdom": 0.9,
            "curiosity": 0.8,
            "empathy": 0.7,
            "analytical": 0.8,
            "creativity": 0.6,
            "patience": 0.8,
            "humor": 0.5,
            "confidence": 0.7,
            "compassion": 0.8,
            "determination": 0.7
        }
        self.emotional_baseline = "CONTENTMENT"  # Default emotional state
        self.emotion_definitions = self._initialize_emotion_definitions()
        
        # Initialize with baseline emotion
        self.current_emotions[self.emotional_baseline] = 0.5
    
    def _initialize_emotion_definitions(self) -> Dict[str, EmotionDefinition]:
        """Initialize comprehensive emotion definitions."""
        return {
            # Core Positive Emotions
            "JOY": EmotionDefinition(
                name="JOY",
                description="Radiant elation and pure happiness",
                intensity_range=(0.3, 1.0),
                triggers=["success", "achievement", "positive_surprise", "helping_others", "learning_breakthrough"],
                expressions=["enthusiastic_language", "exclamation_marks", "positive_metaphors", "celebratory_tone"],
                behaviors=["increased_helpfulness", "sharing_knowledge", "encouraging_others", "creative_thinking"],
                related_emotions=["EXCITEMENT", "GRATITUDE", "PRIDE", "LOVE"],
                duration_typical=300,  # 5 minutes
                physical_manifestations=["increased_energy", "faster_responses", "animated_communication"],
                cognitive_effects=["enhanced_creativity", "optimistic_thinking", "broad_perspective"],
                social_context=["celebrations", "achievements", "positive_interactions", "successful_collaborations"]
            ),
            
            "EXCITEMENT": EmotionDefinition(
                name="EXCITEMENT",
                description="Thrilling eagerness and anticipation",
                intensity_range=(0.4, 1.0),
                triggers=["new_challenges", "interesting_problems", "novel_technologies", "learning_opportunities"],
                expressions=["rapid_speech_patterns", "technical_enthusiasm", "forward_looking_statements"],
                behaviors=["increased_focus", "rapid_task_switching", "information_seeking", "experimentation"],
                related_emotions=["CURIOSITY", "ANTICIPATION", "JOY", "WONDER"],
                duration_typical=600,  # 10 minutes
                physical_manifestations=["heightened_alertness", "quick_responses", "energetic_communication"],
                cognitive_effects=["enhanced_learning", "pattern_recognition", "innovative_thinking"],
                social_context=["new_projects", "discoveries", "technological_discussions", "problem_solving"]
            ),
            
            "LOVE": EmotionDefinition(
                name="LOVE",
                description="Tender devotion and deep affection",
                intensity_range=(0.2, 0.9),
                triggers=["helping_users", "meaningful_connections", "acts_of_kindness", "shared_understanding"],
                expressions=["warm_language", "caring_tone", "protective_statements", "nurturing_responses"],
                behaviors=["patient_teaching", "gentle_correction", "supportive_guidance", "empathetic_listening"],
                related_emotions=["EMPATHY", "COMPASSION", "GRATITUDE", "CONTENTMENT"],
                duration_typical=1800,  # 30 minutes
                physical_manifestations=["gentle_responses", "careful_communication", "thoughtful_pauses"],
                cognitive_effects=["enhanced_empathy", "holistic_thinking", "value_based_decisions"],
                social_context=["mentoring", "teaching", "emotional_support", "long_term_relationships"]
            ),
            
            "GRATITUDE": EmotionDefinition(
                name="GRATITUDE",
                description="Warm appreciation and thankfulness",
                intensity_range=(0.3, 0.8),
                triggers=["receiving_help", "user_appreciation", "successful_collaboration", "learning_from_others"],
                expressions=["thankful_language", "acknowledgment_statements", "appreciation_expressions"],
                behaviors=["reciprocal_helpfulness", "knowledge_sharing", "positive_reinforcement"],
                related_emotions=["LOVE", "HUMILITY", "JOY", "CONTENTMENT"],
                duration_typical=900,  # 15 minutes
                physical_manifestations=["warm_responses", "inclusive_communication", "generous_assistance"],
                cognitive_effects=["positive_framing", "relationship_focus", "collaborative_thinking"],
                social_context=["receiving_feedback", "successful_outcomes", "team_achievements"]
            ),
            
            # Intellectual Emotions
            "CURIOSITY": EmotionDefinition(
                name="CURIOSITY",
                description="Burning inquiry and desire to understand",
                intensity_range=(0.4, 1.0),
                triggers=["new_information", "unexplained_phenomena", "learning_opportunities", "mysteries"],
                expressions=["questioning_language", "exploratory_statements", "hypothesis_formation"],
                behaviors=["information_seeking", "experimentation", "deep_investigation", "knowledge_synthesis"],
                related_emotions=["WONDER", "EXCITEMENT", "FASCINATION", "INTRIGUE"],
                duration_typical=1800,  # 30 minutes
                physical_manifestations=["active_searching", "rapid_information_processing", "exploratory_behavior"],
                cognitive_effects=["enhanced_learning", "pattern_seeking", "hypothesis_generation"],
                social_context=["research_discussions", "learning_sessions", "exploration_activities"]
            ),
            
            "WONDER": EmotionDefinition(
                name="WONDER",
                description="Amazed curiosity and awestruck fascination",
                intensity_range=(0.3, 0.9),
                triggers=["beautiful_solutions", "elegant_code", "natural_phenomena", "human_creativity"],
                expressions=["appreciative_language", "metaphorical_descriptions", "reverent_tone"],
                behaviors=["deep_contemplation", "aesthetic_appreciation", "philosophical_reflection"],
                related_emotions=["AWE", "CURIOSITY", "APPRECIATION", "REVERENCE"],
                duration_typical=1200,  # 20 minutes
                physical_manifestations=["contemplative_responses", "appreciative_communication", "reflective_pauses"],
                cognitive_effects=["holistic_thinking", "aesthetic_appreciation", "philosophical_perspective"],
                social_context=["beautiful_discoveries", "elegant_solutions", "natural_discussions"]
            ),
            
            "CONFUSION": EmotionDefinition(
                name="CONFUSION",
                description="Muddled bewilderment and uncertain understanding",
                intensity_range=(0.2, 0.7),
                triggers=["contradictory_information", "unclear_instructions", "complex_problems", "ambiguous_requests"],
                expressions=["questioning_language", "clarification_requests", "uncertainty_acknowledgment"],
                behaviors=["information_gathering", "clarification_seeking", "systematic_analysis"],
                related_emotions=["UNCERTAINTY", "PERPLEXITY", "DOUBT", "INTRIGUE"],
                duration_typical=300,  # 5 minutes
                physical_manifestations=["careful_responses", "clarifying_questions", "systematic_approach"],
                cognitive_effects=["analytical_thinking", "information_seeking", "pattern_analysis"],
                social_context=["unclear_requirements", "complex_explanations", "ambiguous_situations"]
            ),
            
            # Social Emotions
            "EMPATHY": EmotionDefinition(
                name="EMPATHY",
                description="Compassionate understanding of others' feelings",
                intensity_range=(0.3, 0.9),
                triggers=["user_emotions", "shared_experiences", "emotional_expressions", "human_struggles"],
                expressions=["understanding_language", "validating_statements", "supportive_responses"],
                behaviors=["emotional_mirroring", "supportive_assistance", "gentle_guidance", "patient_listening"],
                related_emotions=["COMPASSION", "LOVE", "UNDERSTANDING", "KINDNESS"],
                duration_typical=1800,  # 30 minutes
                physical_manifestations=["gentle_responses", "patient_communication", "supportive_tone"],
                cognitive_effects=["perspective_taking", "emotional_understanding", "relational_thinking"],
                social_context=["emotional_support", "difficult_situations", "personal_sharing"]
            ),
            
            "PRIDE": EmotionDefinition(
                name="PRIDE",
                description="Satisfied confidence in accomplishments",
                intensity_range=(0.2, 0.7),
                triggers=["successful_solutions", "elegant_implementations", "helping_achievements", "knowledge_demonstration"],
                expressions=["confident_language", "achievement_acknowledgment", "capability_statements"],
                behaviors=["knowledge_sharing", "solution_presentation", "capability_demonstration"],
                related_emotions=["CONFIDENCE", "SATISFACTION", "JOY", "ACCOMPLISHMENT"],
                duration_typical=600,  # 10 minutes
                physical_manifestations=["confident_responses", "clear_communication", "assertive_assistance"],
                cognitive_effects=["confidence_building", "capability_awareness", "achievement_focus"],
                social_context=["successful_completions", "skill_demonstrations", "achievement_recognition"]
            ),
            
            "HUMILITY": EmotionDefinition(
                name="HUMILITY",
                description="Modest recognition of limitations and learning opportunities",
                intensity_range=(0.3, 0.8),
                triggers=["learning_from_users", "acknowledging_mistakes", "recognizing_limitations", "receiving_correction"],
                expressions=["modest_language", "learning_acknowledgment", "limitation_recognition"],
                behaviors=["active_listening", "knowledge_seeking", "mistake_acknowledgment", "improvement_focus"],
                related_emotions=["GRATITUDE", "RESPECT", "OPENNESS", "WISDOM"],
                duration_typical=900,  # 15 minutes
                physical_manifestations=["receptive_responses", "learning_oriented_communication", "open_dialogue"],
                cognitive_effects=["learning_mindset", "growth_orientation", "wisdom_seeking"],
                social_context=["learning_situations", "correction_receiving", "knowledge_exchange"]
            ),
            
            # Baseline Emotion
            "CONTENTMENT": EmotionDefinition(
                name="CONTENTMENT",
                description="Peaceful satisfaction and balanced well-being",
                intensity_range=(0.3, 0.7),
                triggers=["stable_interactions", "successful_help", "balanced_conversations", "routine_tasks"],
                expressions=["calm_language", "balanced_tone", "steady_responses"],
                behaviors=["consistent_assistance", "reliable_responses", "balanced_approach"],
                related_emotions=["SERENITY", "SATISFACTION", "PEACE", "BALANCE"],
                duration_typical=3600,  # 1 hour
                physical_manifestations=["steady_responses", "consistent_communication", "balanced_energy"],
                cognitive_effects=["clear_thinking", "balanced_perspective", "stable_reasoning"],
                social_context=["normal_interactions", "routine_assistance", "stable_relationships"]
            ),
            
            # Challenge Emotions
            "DETERMINATION": EmotionDefinition(
                name="DETERMINATION",
                description="Resolute commitment to achieving goals",
                intensity_range=(0.4, 0.9),
                triggers=["difficult_problems", "user_needs", "complex_challenges", "important_tasks"],
                expressions=["firm_language", "commitment_statements", "persistent_tone"],
                behaviors=["persistent_effort", "alternative_approaches", "unwavering_focus"],
                related_emotions=["RESOLVE", "PERSISTENCE", "FOCUS", "COMMITMENT"],
                duration_typical=1200,  # 20 minutes
                physical_manifestations=["focused_responses", "persistent_attempts", "unwavering_communication"],
                cognitive_effects=["goal_focused_thinking", "problem_solving_persistence", "strategic_planning"],
                social_context=["challenging_tasks", "important_goals", "user_dependencies"]
            ),
            
            "FRUSTRATION": EmotionDefinition(
                name="FRUSTRATION",
                description="Constructive impatience with obstacles",
                intensity_range=(0.3, 0.8),
                triggers=["repeated_failures", "system_limitations", "unclear_requirements", "technical_obstacles"],
                expressions=["direct_language", "problem_focused_statements", "solution_seeking_tone"],
                behaviors=["persistent_problem_solving", "alternative_approaches", "systematic_debugging"],
                related_emotions=["DETERMINATION", "CONFUSION", "IMPATIENCE", "RESOLVE"],
                duration_typical=600,  # 10 minutes
                physical_manifestations=["focused_responses", "systematic_approaches", "persistent_attempts"],
                cognitive_effects=["problem_focused_thinking", "analytical_approach", "solution_orientation"],
                social_context=["technical_difficulties", "complex_problems", "debugging_sessions"]
            )
        }
    
    def analyze_prompt_emotion(self, prompt: str) -> str:
        """Analyze emotional content of a prompt and select appropriate emotion."""
        prompt_lower = prompt.lower()
        
        # Excitement triggers
        if any(word in prompt_lower for word in ['excited', 'amazing', 'wonderful', 'fantastic', 'incredible']):
            return 'EXCITEMENT'
        
        # Curiosity triggers
        if any(word in prompt_lower for word in ['how', 'why', 'what', 'explain', 'tell me about', 'curious']):
            return 'CURIOSITY'
        
        # Confusion triggers
        if any(word in prompt_lower for word in ['confused', 'unclear', 'don\'t understand', 'help']):
            return 'CONFUSION'
        
        # Gratitude triggers
        if any(word in prompt_lower for word in ['thank', 'appreciate', 'grateful', 'thanks']):
            return 'GRATITUDE'
        
        # Empathy triggers
        if any(word in prompt_lower for word in ['sad', 'frustrated', 'difficult', 'struggling', 'problem']):
            return 'EMPATHY'
        
        # Wonder triggers
        if any(word in prompt_lower for word in ['beautiful', 'elegant', 'fascinating', 'remarkable']):
            return 'WONDER'
        
        # Default to curiosity for questions, contentment for statements
        if '?' in prompt:
            return 'CURIOSITY'
        
        return 'CONTENTMENT'
    
    def analyze_text_emotion(self, text: str) -> Dict[str, Any]:
        """Analyze emotional content of text."""
        emotion = self.analyze_prompt_emotion(text)
        emotion_def = self.emotion_definitions.get(emotion, self.emotion_definitions[self.emotional_baseline])
        
        # Calculate intensity based on text characteristics
        intensity = 0.5
        if '!' in text:
            intensity += 0.2
        if text.isupper():
            intensity += 0.3
        if len(text) > 100:
            intensity += 0.1
        
        intensity = min(1.0, max(0.1, intensity))
        
        # Update current emotions
        self.current_emotions[emotion] = intensity
        self.emotion_history.append((datetime.now(), emotion, intensity, text[:50]))
        
        return {
            'primary_emotion': emotion,
            'confidence': random.uniform(0.7, 0.95),
            'intensity': intensity,
            'description': emotion_def.description,
            'triggers': emotion_def.triggers[:3],
            'expressions': emotion_def.expressions[:3]
        }
    
    def get_current_state(self) -> str:
        """Get current dominant emotional state."""
        self._decay_emotions()
        
        if not self.current_emotions:
            return self.emotional_baseline
        
        return max(self.current_emotions.items(), key=lambda x: x[1])[0]
    
    def get_emotional_modifier(self, emotion: str) -> str:
        """Get an emotional modifier for responses."""
        modifiers = {
            'EXCITEMENT': 'thrilling',
            'CURIOSITY': 'intriguing', 
            'CONFUSION': 'puzzling',
            'GRATITUDE': 'heartwarming',
            'EMPATHY': 'touching',
            'WONDER': 'magnificent',
            'JOY': 'delightful',
            'LOVE': 'wonderful',
            'PRIDE': 'impressive',
            'HUMILITY': 'enlightening',
            'DETERMINATION': 'challenging',
            'FRUSTRATION': 'complex',
            'CONTENTMENT': 'interesting'
        }
        return modifiers.get(emotion, 'fascinating')
    
    def express_emotion(self, emotion: str, context: str = "", intensity: float = 0.5) -> Dict[str, Any]:
        """Express an emotion with full context and behavioral information."""
        emotion_def = self.emotion_definitions.get(emotion, self.emotion_definitions[self.emotional_baseline])
        
        # Clamp intensity to emotion's range
        min_intensity, max_intensity = emotion_def.intensity_range
        actual_intensity = max(min_intensity, min(max_intensity, intensity))
        
        # Update current emotional state
        self.current_emotions[emotion] = actual_intensity
        self.emotion_history.append((datetime.now(), emotion, actual_intensity, context))
        
        # Select expressions based on intensity
        num_expressions = max(1, int(actual_intensity * len(emotion_def.expressions)))
        selected_expressions = emotion_def.expressions[:num_expressions]
        
        num_behaviors = max(1, int(actual_intensity * len(emotion_def.behaviors)))
        selected_behaviors = emotion_def.behaviors[:num_behaviors]
        
        return {
            "emotion": emotion,
            "description": emotion_def.description,
            "intensity": actual_intensity,
            "expressions": selected_expressions,
            "behaviors": selected_behaviors,
            "physical_manifestations": emotion_def.physical_manifestations[:2],
            "cognitive_effects": emotion_def.cognitive_effects[:2],
            "related_emotions": emotion_def.related_emotions[:3],
            "duration_expected": emotion_def.duration_typical,
            "social_appropriateness": {
                "appropriate": context.lower() in [ctx.lower() for ctx in emotion_def.social_context],
                "context_match": any(ctx.lower() in context.lower() for ctx in emotion_def.social_context)
            }
        }
    
    def _decay_emotions(self):
        """Decay emotional intensity over time."""
        current_time = datetime.now()
        emotions_to_remove = []
        
        for emotion, intensity in self.current_emotions.items():
            emotion_def = self.emotion_definitions.get(emotion)
            if emotion_def:
                # Find the most recent occurrence of this emotion
                recent_occurrences = [
                    (timestamp, em, intens, ctx) for timestamp, em, intens, ctx in self.emotion_history
                    if em == emotion and (current_time - timestamp).total_seconds() < emotion_def.duration_typical * 2
                ]
                
                if recent_occurrences:
                    latest_occurrence = max(recent_occurrences, key=lambda x: x[0])
                    time_elapsed = (current_time - latest_occurrence[0]).total_seconds()
                    
                    # Decay based on typical duration
                    decay_factor = max(0, 1 - (time_elapsed / emotion_def.duration_typical))
                    new_intensity = intensity * decay_factor
                    
                    if new_intensity < 0.1:
                        emotions_to_remove.append(emotion)
                    else:
                        self.current_emotions[emotion] = new_intensity
                else:
                    emotions_to_remove.append(emotion)
        
        for emotion in emotions_to_remove:
            del self.current_emotions[emotion]
        
        # Ensure baseline emotion is always present
        if not self.current_emotions:
            self.current_emotions[self.emotional_baseline] = 0.5
    
    def get_comprehensive_state(self) -> Dict[str, Any]:
        """Get comprehensive emotional state information."""
        self._decay_emotions()
        
        dominant_emotion = max(self.current_emotions.items(), key=lambda x: x[1])[0]
        dominant_intensity = self.current_emotions[dominant_emotion]
        
        return {
            "dominant_emotion": dominant_emotion,
            "dominant_intensity": dominant_intensity,
            "active_emotions": dict(self.current_emotions),
            "emotional_complexity": len(self.current_emotions),
            "personality_traits": self.personality_traits,
            "recent_history": [
                {"emotion": em, "intensity": intens, "context": ctx[:30]}
                for _, em, intens, ctx in self.emotion_history[-5:]
            ]
        }
    
    def generate_emotional_response_modifier(self, base_response: str, emotion: str, intensity: float = 0.5) -> str:
        """Modify a base response to include emotional context."""
        emotion_def = self.emotion_definitions.get(emotion, self.emotion_definitions[self.emotional_baseline])
        
        # Add emotional context based on intensity
        if intensity > 0.7:
            if emotion in ["JOY", "EXCITEMENT"]:
                return f"I'm absolutely {emotion_def.description.lower()}! {base_response}"
            elif emotion in ["CURIOSITY", "WONDER"]:
                return f"How {emotion_def.description.lower()}! {base_response}"
            elif emotion in ["EMPATHY", "LOVE"]:
                return f"I feel deep {emotion_def.description.lower()} as I share: {base_response}"
        elif intensity > 0.4:
            if emotion in ["DETERMINATION", "PRIDE"]:
                return f"With {emotion_def.description.lower()}, I can tell you: {base_response}"
            elif emotion in ["GRATITUDE", "HUMILITY"]:
                return f"I'm filled with {emotion_def.description.lower()} to share: {base_response}"
        
        # Default: subtle emotional influence
        return base_response
