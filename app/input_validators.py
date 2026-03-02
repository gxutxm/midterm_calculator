"""Input validation utilities."""

from app.exceptions import ValidationError


class InputValidator:
    """Validates user input for the calculator."""
    
    def __init__(self, max_value: int = 1000000):
        """
        Initialize validator.
        
        Args:
            max_value: Maximum allowed input value
        """
        self.max_value = max_value
    
    def validate_number(self, value: str) -> float:
        """
        Validate and convert string to number.
        
        Args:
            value: String to validate
            
        Returns:
            Float value
            
        Raises:
            ValidationError: If value is invalid
        """
        try:
            num = float(value)
        except ValueError:
            raise ValidationError(f"'{value}' is not a valid number")
        
        if abs(num) > self.max_value:
            raise ValidationError(
                f"Value {num} exceeds maximum allowed value of {self.max_value}"
            )
        
        return num
    
    def validate_operation(self, operation: str, available_operations: list) -> str:
        """
        Validate operation name.
        
        Args:
            operation: Operation name to validate
            available_operations: List of valid operations
            
        Returns:
            Lowercase operation name
            
        Raises:
            ValidationError: If operation is invalid
        """
        operation = operation.lower().strip()
        
        if not operation:
            raise ValidationError("Operation cannot be empty")
        
        if operation not in available_operations:
            available = ', '.join(available_operations)
            raise ValidationError(
                f"Unknown operation: '{operation}'. "
                f"Available: {available}"
            )
        
        return operation