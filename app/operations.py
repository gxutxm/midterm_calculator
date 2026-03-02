"""
Operations module with Strategy and Factory patterns.

Implements 10 arithmetic operations as strategies.
"""

from abc import ABC, abstractmethod
from typing import Dict, Type
from app.exceptions import DivisionByZeroError, OperationError


class OperationStrategy(ABC):
    """Base class for all operations using Strategy pattern."""
    
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        """Perform the operation on two numbers."""
        pass
    
    @property
    @abstractmethod
    def symbol(self) -> str:
        """Return the symbol for this operation."""
        pass


class AddOperation(OperationStrategy):
    """Addition operation."""
    
    def execute(self, a: float, b: float) -> float:
        return a + b
    
    @property
    def symbol(self) -> str:
        return "+"


class SubtractOperation(OperationStrategy):
    """Subtraction operation."""
    
    def execute(self, a: float, b: float) -> float:
        return a - b
    
    @property
    def symbol(self) -> str:
        return "-"


class MultiplyOperation(OperationStrategy):
    """Multiplication operation."""
    
    def execute(self, a: float, b: float) -> float:
        return a * b
    
    @property
    def symbol(self) -> str:
        return "×"


class DivideOperation(OperationStrategy):
    """Division operation with zero check."""
    
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise DivisionByZeroError("Cannot divide by zero")
        return a / b
    
    @property
    def symbol(self) -> str:
        return "÷"


class PowerOperation(OperationStrategy):
    """Power operation (a^b)."""
    
    def execute(self, a: float, b: float) -> float:
        return a ** b
    
    @property
    def symbol(self) -> str:
        return "^"


class RootOperation(OperationStrategy):
    """Root operation (b-th root of a)."""
    
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise DivisionByZeroError("Cannot calculate 0-th root")
        if a < 0 and b % 2 == 0:
            raise OperationError("Cannot calculate even root of negative number")
        return a ** (1 / b)
    
    @property
    def symbol(self) -> str:
        return "√"


class ModulusOperation(OperationStrategy):
    """Modulus operation (remainder of a/b)."""
    
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise DivisionByZeroError("Cannot calculate modulus with zero divisor")
        return a % b
    
    @property
    def symbol(self) -> str:
        return "%"


class IntDivideOperation(OperationStrategy):
    """Integer division operation (a // b)."""
    
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise DivisionByZeroError("Cannot divide by zero")
        return a // b
    
    @property
    def symbol(self) -> str:
        return "//"


class PercentOperation(OperationStrategy):
    """Percentage calculation (a/b * 100)."""
    
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise DivisionByZeroError("Cannot calculate percentage with zero denominator")
        return (a / b) * 100
    
    @property
    def symbol(self) -> str:
        return "%of"


class AbsDiffOperation(OperationStrategy):
    """Absolute difference operation (|a - b|)."""
    
    def execute(self, a: float, b: float) -> float:
        return abs(a - b)
    
    @property
    def symbol(self) -> str:
        return "|Δ|"


class OperationFactory:
    """
    Factory for creating operation strategies.
    
    Implements Factory pattern to centralize operation creation.
    """
    
    _operations: Dict[str, Type[OperationStrategy]] = {
        'add': AddOperation,
        'subtract': SubtractOperation,
        'multiply': MultiplyOperation,
        'divide': DivideOperation,
        'power': PowerOperation,
        'root': RootOperation,
        'modulus': ModulusOperation,
        'int_divide': IntDivideOperation,
        'percent': PercentOperation,
        'abs_diff': AbsDiffOperation,
    }
    
    @classmethod
    def create_operation(cls, operation_name: str) -> OperationStrategy:
        """
        Create an operation by name.
        
        Args:
            operation_name: Name of the operation
            
        Returns:
            Instance of the operation strategy
            
        Raises:
            OperationError: If operation name is unknown
        """
        operation_class = cls._operations.get(operation_name.lower())
        
        if operation_class is None:
            available = ', '.join(cls._operations.keys())
            raise OperationError(
                f"Unknown operation: '{operation_name}'. "
                f"Available: {available}"
            )
        
        return operation_class()
    
    @classmethod
    def get_available_operations(cls) -> list:
        """Get list of available operation names."""
        return list(cls._operations.keys())