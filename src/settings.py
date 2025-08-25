import json
import os
from typing import Dict, Any

class AppSettings:
    """Application settings and thresholds"""
    
    SETTINGS_FILE = 'config/settings.json'
    
    # Default values
    _defaults = {
        'TEMPERATURE_THRESHOLD': 38.0,
        'HEART_RATE_THRESHOLD': 100,
        'GFORCE_THRESHOLD': 3.0,
        'UPDATE_INTERVAL': 1000
    }
    
    def __init__(self):
        self._settings = self._load_settings()
    
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file or create with defaults"""
        if os.path.exists(self.SETTINGS_FILE):
            try:
                with open(self.SETTINGS_FILE, 'r') as f:
                    settings = json.load(f)
                # Merge with defaults to handle new settings
                return {**self._defaults, **settings}
            except (json.JSONDecodeError, IOError):
                pass
        
        # Create directory and file with defaults
        os.makedirs(os.path.dirname(self.SETTINGS_FILE), exist_ok=True)
        self._save_settings(self._defaults)
        return self._defaults.copy()
    
    def _save_settings(self, settings: Dict[str, Any]):
        """Save settings to file"""
        with open(self.SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
    
    def update_settings(self, **kwargs):
        """Update settings and save to file"""
        for key, value in kwargs.items():
            if key in self._defaults:
                self._settings[key] = value
        self._save_settings(self._settings)
    
    @property
    def TEMPERATURE_THRESHOLD(self) -> float:
        return self._settings['TEMPERATURE_THRESHOLD']
    
    @property
    def HEART_RATE_THRESHOLD(self) -> int:
        return self._settings['HEART_RATE_THRESHOLD']
    
    @property
    def GFORCE_THRESHOLD(self) -> float:
        return self._settings['GFORCE_THRESHOLD']
    
    @property
    def UPDATE_INTERVAL(self) -> int:
        return self._settings['UPDATE_INTERVAL']
    
    def is_temperature_warning(self, temperature: float) -> bool:
        return temperature > self.TEMPERATURE_THRESHOLD
    
    def is_heart_rate_warning(self, heart_rate: int) -> bool:
        return heart_rate > self.HEART_RATE_THRESHOLD
    
    def is_gforce_warning(self, gforce: float) -> bool:
        return gforce > self.GFORCE_THRESHOLD
    
    def to_dict(self) -> Dict[str, Any]:
        """Return settings as dictionary for JSON serialization"""
        return self._settings.copy()

# Global settings instance
app_settings = AppSettings()