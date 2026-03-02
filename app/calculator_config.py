"""Configuration management for calculator."""

import os
from pathlib import Path
from dotenv import load_dotenv
from app.exceptions import ConfigurationError


class CalculatorConfig:
    """Manages calculator configuration from environment variables."""
    
    def __init__(self):
        """Load configuration from .env file."""
        load_dotenv()
        self._load_settings()
        self.validate()
    
    def _load_settings(self):
        """Load all settings from environment variables."""
        # Directories
        self.log_dir = Path(os.getenv('CALCULATOR_LOG_DIR', 'logs/'))
        self.history_dir = Path(os.getenv('CALCULATOR_HISTORY_DIR', 'history/'))
        
        # Create directories if they don't exist
        self.log_dir.mkdir(exist_ok=True)
        self.history_dir.mkdir(exist_ok=True)
        
        # History settings
        self.max_history_size = self._get_int('CALCULATOR_MAX_HISTORY_SIZE', 1000)
        self.auto_save = os.getenv('CALCULATOR_AUTO_SAVE', 'true').lower() == 'true'
        
        # Calculation settings
        self.precision = self._get_int('CALCULATOR_PRECISION', 2)
        self.max_input_value = self._get_int('CALCULATOR_MAX_INPUT_VALUE', 1000000)
        self.default_encoding = os.getenv('CALCULATOR_DEFAULT_ENCODING', 'utf-8')
        
        # File paths
        self.history_file = self.history_dir / 'calculation_history.csv'
    
    def _get_int(self, key: str, default: int) -> int:
        """Get integer setting from environment."""
        value = os.getenv(key, str(default))
        try:
            return int(value)
        except ValueError:
            raise ConfigurationError(f"Invalid value for {key}: '{value}'")
    
    def validate(self):
        """Validate configuration settings."""
        if self.max_history_size <= 0:
            raise ConfigurationError("MAX_HISTORY_SIZE must be positive")
        
        if self.precision < 0:
            raise ConfigurationError("PRECISION must be non-negative")
        
        if self.max_input_value <= 0:
            raise ConfigurationError("MAX_INPUT_VALUE must be positive")
    
    def __str__(self):
        """Return string representation of configuration."""
        return (
            f"Configuration:\n"
            f"  Log Dir: {self.log_dir}\n"
            f"  History Dir: {self.history_dir}\n"
            f"  Max History Size: {self.max_history_size}\n"
            f"  Auto Save: {self.auto_save}\n"
            f"  Precision: {self.precision}\n"
            f"  Max Input Value: {self.max_input_value}"
        )