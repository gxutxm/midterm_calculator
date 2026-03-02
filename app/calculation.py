"""Calculation class with Factory pattern."""

from datetime import datetime
from typing import Optional
from app.operations import OperationStrategy, OperationFactory
from app.exceptions import OperationError


class Calculation:
    """Represents a single calculation with timestamp."""
    
    def __init__(self, operation_name: str, operand_a: float, operand_b: float):
        """
        Create a new calculation.
        
        Args:
            operation_name: Name of operation
            operand_a: First number
            operand_b: Second number
        """
        self.operation_name = operation_name
        self.operand_a = operand_a
        self.operand_b = operand_b
        self._result: Optional[float] = None
        self.timestamp = datetime.now()
        
        # Use factory to get the operation
        self.operation: OperationStrategy = OperationFactory.create_operation(operation_name)
    
    def execute(self) -> float:
        """
        Execute the calculation and return result.
        
        Returns:
            Calculation result
            
        Raises:
            OperationError: If calculation fails
        """
        try:
            self._result = self.operation.execute(self.operand_a, self.operand_b)
            return self._result
        except Exception as e:
            raise OperationError(f"Calculation failed: {e}")
    
    def get_result(self) -> Optional[float]:
        """Get the result if calculation was executed."""
        return self._result
    
    def to_dict(self) -> dict:
        """Convert calculation to dictionary for storage."""
        return {
            'operation': self.operation_name,
            'operand_a': self.operand_a,
            'operand_b': self.operand_b,
            'result': self._result,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Calculation':
        """
        Create calculation from dictionary.
        
        Args:
            data: Dictionary with calculation data
            
        Returns:
            Calculation instance
        """
        calc = cls(data['operation'], data['operand_a'], data['operand_b'])
        calc._result = data['result']
        
        # Parse timestamp if present
        if 'timestamp' in data:
            calc.timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
        
        return calc
    
    def __str__(self) -> str:
        """Return string representation of calculation."""
        symbol = self.operation.symbol
        
        if self._result is not None:
            return f"{self.operand_a} {symbol} {self.operand_b} = {self._result}"
        return f"{self.operand_a} {symbol} {self.operand_b}"
    
    def __repr__(self) -> str:
        """Return detailed representation for debugging."""
        return f"Calculation({self.operation_name}, {self.operand_a}, {self.operand_b})"