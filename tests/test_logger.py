"""Tests for logger module."""

import pytest
from pathlib import Path
from app.logger import CalculatorLogger, get_logger


class TestCalculatorLogger:
    def test_logger_initialization(self, tmp_path):
        logger = CalculatorLogger(str(tmp_path), "INFO")
        assert logger.logger is not None
        assert logger.log_dir == tmp_path
    
    def test_log_calculation(self, tmp_path):
        logger = CalculatorLogger(str(tmp_path), "INFO")
        logger.log_calculation('add', 5, 3, 8)
        
        # Check log file was created
        log_files = list(tmp_path.glob("*.log"))
        assert len(log_files) > 0
    
    def test_log_error(self, tmp_path):
        logger = CalculatorLogger(str(tmp_path), "INFO")
        logger.log_error("Test error message")
        
        log_files = list(tmp_path.glob("*.log"))
        assert len(log_files) > 0
    
    def test_log_info(self, tmp_path):
        logger = CalculatorLogger(str(tmp_path), "INFO")
        logger.log_info("Test info message")
        
        log_files = list(tmp_path.glob("*.log"))
        assert len(log_files) > 0
    
    def test_log_warning(self, tmp_path):
        logger = CalculatorLogger(str(tmp_path), "INFO")
        logger.log_warning("Test warning message")
        
        log_files = list(tmp_path.glob("*.log"))
        assert len(log_files) > 0
    
    def test_log_debug(self, tmp_path):
        logger = CalculatorLogger(str(tmp_path), "DEBUG")
        logger.log_debug("Test debug message")
        
        log_files = list(tmp_path.glob("*.log"))
        assert len(log_files) > 0


class TestGetLogger:
    def test_get_logger_singleton(self, tmp_path):
        logger1 = get_logger(str(tmp_path), "INFO")
        logger2 = get_logger(str(tmp_path), "INFO")
        assert logger1 is logger2