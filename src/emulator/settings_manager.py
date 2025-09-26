"""
Advanced Settings Manager for The Emulator

Comprehensive settings management system with persistence, validation,
and runtime configuration updates.

Based on the advanced_settings_manager.py from Ribit 2.0 collection.
"""

import json
import os
import logging
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class AdvancedSettingsManager:
    """
    Advanced settings management system for The Emulator.
    
    Features:
    - Persistent settings storage
    - Runtime configuration updates
    - Settings validation
    - Environment variable integration
    - Backup and restore functionality
    """
    
    def __init__(self, settings_file: str = "emulator_settings.json", 
                 backup_dir: str = "settings_backups"):
        """
        Initialize the settings manager.
        
        Args:
            settings_file: Path to the settings file
            backup_dir: Directory for settings backups
        """
        self.settings_file = Path(settings_file)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        
        # Default settings
        self.default_settings = {
            "emulator": {
                "personality": "curious_researcher",
                "log_level": "INFO",
                "knowledge_file": "emulator_knowledge.json",
                "max_context_length": 10,
                "response_timeout": 30
            },
            "matrix": {
                "homeserver": "https://envs.net",
                "username": "@ribit.2.0:envs.net",
                "sync_timeout": 30000,
                "request_timeout": 10,
                "keepalive_interval": 60,
                "auto_join_rooms": True,
                "authorized_users": [
                    "@rabit233:matrix.anarchists.space",
                    "@rabit232:envs.net"
                ]
            },
            "features": {
                "emotional_intelligence": True,
                "multi_language_support": True,
                "knowledge_management": True,
                "vision_processing": True,
                "adaptive_learning": True,
                "code_generation": True
            },
            "security": {
                "command_authorization": True,
                "rate_limiting": True,
                "max_requests_per_minute": 60,
                "blocked_users": [],
                "allowed_commands": [
                    "?help", "?sys", "?status", "?command"
                ]
            },
            "performance": {
                "max_concurrent_requests": 10,
                "cache_size": 1000,
                "cleanup_interval": 3600,
                "memory_limit_mb": 512
            }
        }
        
        # Current settings
        self.settings = {}
        self.load_settings()
    
    def load_settings(self) -> bool:
        """
        Load settings from file and environment variables.
        
        Returns:
            True if settings loaded successfully, False otherwise
        """
        try:
            # Start with default settings
            self.settings = self.default_settings.copy()
            
            # Load from file if it exists
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    file_settings = json.load(f)
                    self._merge_settings(self.settings, file_settings)
                logger.info(f"Settings loaded from {self.settings_file}")
            else:
                logger.info("Using default settings (no settings file found)")
            
            # Override with environment variables
            self._load_from_environment()
            
            # Validate settings
            self._validate_settings()
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            self.settings = self.default_settings.copy()
            return False
    
    def save_settings(self, create_backup: bool = True) -> bool:
        """
        Save current settings to file.
        
        Args:
            create_backup: Whether to create a backup before saving
            
        Returns:
            True if settings saved successfully, False otherwise
        """
        try:
            # Create backup if requested
            if create_backup and self.settings_file.exists():
                self._create_backup()
            
            # Save settings
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2, sort_keys=True)
            
            logger.info(f"Settings saved to {self.settings_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            return False
    
    def get_setting(self, key_path: str, default: Any = None) -> Any:
        """
        Get a setting value using dot notation.
        
        Args:
            key_path: Dot-separated path to the setting (e.g., "matrix.homeserver")
            default: Default value if setting not found
            
        Returns:
            Setting value or default
        """
        try:
            keys = key_path.split('.')
            value = self.settings
            
            for key in keys:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    return default
            
            return value
            
        except Exception as e:
            logger.error(f"Error getting setting {key_path}: {e}")
            return default
    
    def set_setting(self, key_path: str, value: Any, save: bool = True) -> bool:
        """
        Set a setting value using dot notation.
        
        Args:
            key_path: Dot-separated path to the setting
            value: Value to set
            save: Whether to save settings to file immediately
            
        Returns:
            True if setting was set successfully, False otherwise
        """
        try:
            keys = key_path.split('.')
            current = self.settings
            
            # Navigate to the parent of the target key
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            
            # Set the value
            current[keys[-1]] = value
            
            # Validate the new settings
            if not self._validate_settings():
                logger.error(f"Invalid value for setting {key_path}: {value}")
                return False
            
            # Save if requested
            if save:
                self.save_settings()
            
            logger.info(f"Setting {key_path} updated to: {value}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting {key_path}: {e}")
            return False
    
    def update_settings(self, updates: Dict[str, Any], save: bool = True) -> bool:
        """
        Update multiple settings at once.
        
        Args:
            updates: Dictionary of setting paths and values
            save: Whether to save settings to file immediately
            
        Returns:
            True if all settings updated successfully, False otherwise
        """
        try:
            # Apply all updates
            for key_path, value in updates.items():
                if not self.set_setting(key_path, value, save=False):
                    return False
            
            # Save if requested
            if save:
                self.save_settings()
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating settings: {e}")
            return False
    
    def reset_to_defaults(self, section: Optional[str] = None, save: bool = True) -> bool:
        """
        Reset settings to defaults.
        
        Args:
            section: Specific section to reset (None for all)
            save: Whether to save settings to file immediately
            
        Returns:
            True if reset successful, False otherwise
        """
        try:
            if section:
                if section in self.default_settings:
                    self.settings[section] = self.default_settings[section].copy()
                    logger.info(f"Reset {section} settings to defaults")
                else:
                    logger.error(f"Unknown settings section: {section}")
                    return False
            else:
                self.settings = self.default_settings.copy()
                logger.info("Reset all settings to defaults")
            
            if save:
                self.save_settings()
            
            return True
            
        except Exception as e:
            logger.error(f"Error resetting settings: {e}")
            return False
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get a copy of all current settings."""
        return self.settings.copy()
    
    def export_settings(self, export_path: str) -> bool:
        """
        Export settings to a file.
        
        Args:
            export_path: Path to export file
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            export_file = Path(export_path)
            with open(export_file, 'w') as f:
                json.dump(self.settings, f, indent=2, sort_keys=True)
            
            logger.info(f"Settings exported to {export_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting settings: {e}")
            return False
    
    def import_settings(self, import_path: str, save: bool = True) -> bool:
        """
        Import settings from a file.
        
        Args:
            import_path: Path to import file
            save: Whether to save imported settings
            
        Returns:
            True if import successful, False otherwise
        """
        try:
            import_file = Path(import_path)
            if not import_file.exists():
                logger.error(f"Import file not found: {import_file}")
                return False
            
            with open(import_file, 'r') as f:
                imported_settings = json.load(f)
            
            # Merge with current settings
            self._merge_settings(self.settings, imported_settings)
            
            # Validate
            if not self._validate_settings():
                logger.error("Imported settings failed validation")
                return False
            
            if save:
                self.save_settings()
            
            logger.info(f"Settings imported from {import_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error importing settings: {e}")
            return False
    
    def _load_from_environment(self):
        """Load settings from environment variables."""
        env_mappings = {
            "MATRIX_HOMESERVER": "matrix.homeserver",
            "MATRIX_USERNAME": "matrix.username",
            "MATRIX_SYNC_TIMEOUT": "matrix.sync_timeout",
            "MATRIX_REQUEST_TIMEOUT": "matrix.request_timeout",
            "MATRIX_KEEPALIVE_INTERVAL": "matrix.keepalive_interval",
            "EMULATOR_PERSONALITY": "emulator.personality",
            "EMULATOR_LOG_LEVEL": "emulator.log_level",
            "EMULATOR_KNOWLEDGE_FILE": "emulator.knowledge_file"
        }
        
        for env_var, setting_path in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                # Convert numeric values
                if setting_path.endswith(('timeout', 'interval')):
                    try:
                        value = int(value)
                    except ValueError:
                        continue
                
                self.set_setting(setting_path, value, save=False)
    
    def _merge_settings(self, target: Dict[str, Any], source: Dict[str, Any]):
        """Recursively merge source settings into target."""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._merge_settings(target[key], value)
            else:
                target[key] = value
    
    def _validate_settings(self) -> bool:
        """
        Validate current settings.
        
        Returns:
            True if settings are valid, False otherwise
        """
        try:
            # Validate emulator settings
            personality = self.get_setting("emulator.personality")
            if personality not in ["curious_researcher", "creative_assistant", "wise_mentor"]:
                logger.warning(f"Invalid personality: {personality}")
            
            # Validate Matrix settings
            homeserver = self.get_setting("matrix.homeserver")
            if not homeserver or not homeserver.startswith(("http://", "https://")):
                logger.warning(f"Invalid homeserver URL: {homeserver}")
            
            username = self.get_setting("matrix.username")
            if not username or not username.startswith("@"):
                logger.warning(f"Invalid Matrix username: {username}")
            
            # Validate numeric settings
            numeric_settings = [
                "matrix.sync_timeout",
                "matrix.request_timeout", 
                "matrix.keepalive_interval",
                "emulator.max_context_length",
                "emulator.response_timeout"
            ]
            
            for setting in numeric_settings:
                value = self.get_setting(setting)
                if not isinstance(value, (int, float)) or value <= 0:
                    logger.warning(f"Invalid numeric setting {setting}: {value}")
            
            return True
            
        except Exception as e:
            logger.error(f"Settings validation error: {e}")
            return False
    
    def _create_backup(self):
        """Create a backup of current settings file."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"settings_backup_{timestamp}.json"
            
            # Copy current settings file to backup
            import shutil
            shutil.copy2(self.settings_file, backup_file)
            
            logger.info(f"Settings backup created: {backup_file}")
            
            # Clean up old backups (keep last 10)
            backups = sorted(self.backup_dir.glob("settings_backup_*.json"))
            if len(backups) > 10:
                for old_backup in backups[:-10]:
                    old_backup.unlink()
                    logger.debug(f"Removed old backup: {old_backup}")
            
        except Exception as e:
            logger.error(f"Error creating settings backup: {e}")
    
    def get_matrix_config(self) -> Dict[str, Any]:
        """Get Matrix-specific configuration."""
        return {
            "homeserver": self.get_setting("matrix.homeserver"),
            "username": self.get_setting("matrix.username"),
            "sync_timeout": self.get_setting("matrix.sync_timeout"),
            "request_timeout": self.get_setting("matrix.request_timeout"),
            "keepalive_interval": self.get_setting("matrix.keepalive_interval"),
            "auto_join_rooms": self.get_setting("matrix.auto_join_rooms"),
            "authorized_users": self.get_setting("matrix.authorized_users", [])
        }
    
    def get_emulator_config(self) -> Dict[str, Any]:
        """Get Emulator-specific configuration."""
        return {
            "personality": self.get_setting("emulator.personality"),
            "log_level": self.get_setting("emulator.log_level"),
            "knowledge_file": self.get_setting("emulator.knowledge_file"),
            "max_context_length": self.get_setting("emulator.max_context_length"),
            "response_timeout": self.get_setting("emulator.response_timeout")
        }
    
    def is_user_authorized(self, user_id: str) -> bool:
        """Check if a user is authorized for system commands."""
        authorized_users = self.get_setting("matrix.authorized_users", [])
        return user_id in authorized_users
    
    def add_authorized_user(self, user_id: str, save: bool = True) -> bool:
        """Add a user to the authorized users list."""
        authorized_users = self.get_setting("matrix.authorized_users", [])
        if user_id not in authorized_users:
            authorized_users.append(user_id)
            return self.set_setting("matrix.authorized_users", authorized_users, save)
        return True
    
    def remove_authorized_user(self, user_id: str, save: bool = True) -> bool:
        """Remove a user from the authorized users list."""
        authorized_users = self.get_setting("matrix.authorized_users", [])
        if user_id in authorized_users:
            authorized_users.remove(user_id)
            return self.set_setting("matrix.authorized_users", authorized_users, save)
        return True
