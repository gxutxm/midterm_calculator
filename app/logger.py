"""
Logging module for the calculator.

Handles all logging to files with proper formatting and levels.
"""

import logging
import os
from datetime import datetime
from pathlib import Path


class CalculatorLogger:
    """
    Manages logging for calculator operations.
    
    Logs calculations, errors, and events to a file.
    """
    
    def __init__(self, log_dir: str = "logs/", log_level: str = "INFO"):
        """
        Initialize logger.
        
        Args:
            log_dir: Directory for log files
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create log filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file = self.log_dir / f"calculator_{timestamp}.log"
        
        # Configure logger
        self.logger = logging.getLogger("CalculatorLogger")
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, log_level.upper()))
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
    
    def log_calculation(self, operation: str, operand_a: float, operand_b: float, result: float):
        """Log a calculation."""
        self.logger.info(
            f"Calculation: {operation}({operand_a}, {operand_b}) = {result}"
        )
    
    def log_error(self, error_message: str):
        """Log an error."""
        self.logger.error(f"Error: {error_message}")
    
    def log_info(self, message: str):
        """Log general information."""
        self.logger.info(message)
    
    def log_warning(self, message: str):
        """Log a warning."""
        self.logger.warning(message)
    
    def log_debug(self, message: str):
        """Log debug information."""
        self.logger.debug(message)


# Create a global logger instance
_logger_instance = None


def get_logger(log_dir: str = "logs/", log_level: str = "INFO") -> CalculatorLogger:
    """
    Get the global logger instance.
    
    Creates one if it doesn't exist (Singleton pattern).
    """
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = CalculatorLogger(log_dir, log_level)
    return _logger_instance