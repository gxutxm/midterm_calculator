"""Tests for custom exceptions."""

import pytest
from app.exceptions import (
    CalculatorError, OperationError, ValidationError,
    DivisionByZeroError, HistoryError, ConfigurationError, MementoError
)


def test_calculator_error_is_base():
    """Test that CalculatorError is base exception."""
    error = CalculatorError("test")
    assert isinstance(error, Exception)
    assert str(error) == "test"


def test_operation_error():
    """Test OperationError."""
    error = OperationError("operation failed")
    assert isinstance(error, CalculatorError)


def test_validation_error():
    """Test ValidationError."""
    error = ValidationError("invalid input")
    assert isinstance(error, CalculatorError)


def test_division_by_zero_error():
    """Test DivisionByZeroError."""
    error = DivisionByZeroError("cannot divide by zero")
    assert isinstance(error, CalculatorError)


def test_history_error():
    """Test HistoryError."""
    error = HistoryError("history error")
    assert isinstance(error, CalculatorError)


def test_configuration_error():
    """Test ConfigurationError."""
    error = ConfigurationError("config error")
    assert isinstance(error, CalculatorError)


def test_memento_error():
    """Test MementoError."""
    error = MementoError("memento error")
    assert isinstance(error, CalculatorError)
    