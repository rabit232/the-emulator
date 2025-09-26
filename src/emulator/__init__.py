"""
The Emulator - Advanced LLM Emulation System

A sophisticated AI emulation system with emotional intelligence,
multi-language programming support, Matrix bot integration,
and advanced reasoning capabilities.

Author: rabit232
License: MIT
"""

from .core import AdvancedLLMEmulator
from .emotions import EmotionalIntelligence
from .languages import MultiLanguageSupport
from .knowledge import KnowledgeManager
from .settings_manager import AdvancedSettingsManager

# Matrix bot import (optional, graceful fallback if dependencies missing)
try:
    from .matrix_bot import EmulatorMatrixBot
    MATRIX_AVAILABLE = True
except ImportError:
    MATRIX_AVAILABLE = False
    EmulatorMatrixBot = None

__version__ = "1.1.0"
__author__ = "rabit232"
__license__ = "MIT"

__all__ = [
    "AdvancedLLMEmulator",
    "EmotionalIntelligence", 
    "MultiLanguageSupport",
    "KnowledgeManager",
    "AdvancedSettingsManager",
    "EmulatorMatrixBot",
    "MATRIX_AVAILABLE"
]
