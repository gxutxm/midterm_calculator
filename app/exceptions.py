"""Custom exceptions for the calculator."""


class CalculatorError(Exception):
    """Base exception for calculator errors."""
    pass


class OperationError(CalculatorError):
    """Raised when an operation fails."""
    pass


class ValidationError(CalculatorError):
    """Raised when input validation fails."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when dividing by zero."""
    pass


class HistoryError(CalculatorError):
    """Raised when history operations fail."""
    pass


class ConfigurationError(CalculatorError):
    """Raised when configuration is invalid."""
    pass


class MementoError(CalculatorError):
    """Raised when undo/redo fails."""
    pass