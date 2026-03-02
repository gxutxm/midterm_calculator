"""Tests for configuration management."""

import pytest
import os
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


class TestCalculatorConfig:
    def test_config_loads_defaults(self):
        config = CalculatorConfig()
        assert config.log_dir is not None
        assert config.history_dir is not None
        assert config.max_history_size > 0
        assert isinstance(config.auto_save, bool)
    
    def test_config_validates_successfully(self):
        config = CalculatorConfig()
        config.validate()  # Should not raise error
    
    def test_invalid_max_history_size(self):
        config = CalculatorConfig()
        config.max_history_size = -1
        with pytest.raises(ConfigurationError):
            config.validate()
    
    def test_invalid_precision(self):
        config = CalculatorConfig()
        config.precision = -1
        with pytest.raises(ConfigurationError):
            config.validate()
    
    def test_invalid_max_input_value(self):
        config = CalculatorConfig()
        config.max_input_value = 0
        with pytest.raises(ConfigurationError):
            config.validate()
    
    def test_config_string_representation(self):
        config = CalculatorConfig()
        config_str = str(config)
        assert 'Configuration:' in config_str
        assert 'Log Dir:' in config_str