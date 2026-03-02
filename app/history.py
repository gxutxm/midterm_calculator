"""History management with pandas and Observer pattern."""

import pandas as pd
from typing import List
from pathlib import Path
from app.calculation import Calculation
from app.exceptions import HistoryError
from app.logger import get_logger


class HistoryObserver:
    """Base class for history observers using Observer pattern."""
    
    def update(self, calculation: Calculation):
        """Called when a new calculation is added."""
        pass


class LoggingObserver(HistoryObserver):
    """Observer that logs calculations to file."""
    
    def __init__(self, log_dir: str = "logs/"):
        """Initialize with logger."""
        self.logger = get_logger(log_dir)
    
    def update(self, calculation: Calculation):
        """Log the calculation."""
        self.logger.log_calculation(
            calculation.operation_name,
            calculation.operand_a,
            calculation.operand_b,
            calculation.get_result()
        )


class AutoSaveObserver(HistoryObserver):
    """Observer that auto-saves history to CSV."""
    
    def __init__(self, history_file: Path):
        """
        Initialize with history file path.
        
        Args:
            history_file: Path to CSV file
        """
        self.history_file = history_file
        self.history_reference = None
    
    def set_history(self, history):
        """Set reference to history object."""
        self.history_reference = history
    
    def update(self, calculation: Calculation):
        """Auto-save history when calculation is added."""
        if self.history_reference:
            self.history_reference.save_to_csv(str(self.history_file))


class CalculationHistory:
    """
    Manages calculation history using pandas DataFrame.
    
    Implements Observer pattern for logging and auto-save.
    """
    
    def __init__(self, max_size: int = 1000):
        """
        Create empty history.
        
        Args:
            max_size: Maximum number of calculations to store
        """
        self.max_size = max_size
        self.history = pd.DataFrame(columns=['operation', 'operand_a', 'operand_b', 'result', 'timestamp'])
        self._observers: List[HistoryObserver] = []
    
    def add_calculation(self, calculation: Calculation):
        """
        Add a calculation to history.
        
        Args:
            calculation: Calculation to add
        """
        calc_dict = calculation.to_dict()
        
        # Add to DataFrame
        new_row = pd.DataFrame([calc_dict])
        self.history = pd.concat([self.history, new_row], ignore_index=True)
        
        # Trim history if exceeds max size
        if len(self.history) > self.max_size:
            self.history = self.history.tail(self.max_size)
        
        # Notify observers
        self._notify_observers(calculation)
    
    def get_all(self) -> pd.DataFrame:
        """Get all history as DataFrame."""
        return self.history.copy()
    
    def get_last(self) -> dict:
        """
        Get the last calculation.
        
        Returns:
            Dictionary with calculation data
            
        Raises:
            HistoryError: If history is empty
        """
        if len(self.history) == 0:
            raise HistoryError("No calculations in history")
        
        return self.history.iloc[-1].to_dict()
    
    def clear(self):
        """Clear all history."""
        self.history = pd.DataFrame(columns=['operation', 'operand_a', 'operand_b', 'result', 'timestamp'])
    
    def save_to_csv(self, filename: str):
        """
        Save history to CSV file using pandas.
        
        Args:
            filename: Path to CSV file
        """
        try:
            filepath = Path(filename)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            self.history.to_csv(filepath, index=False)
        except Exception as e:
            raise HistoryError(f"Failed to save history: {e}")
    
    def load_from_csv(self, filename: str):
        """
        Load history from CSV file using pandas.
        
        Args:
            filename: Path to CSV file
        """
        try:
            filepath = Path(filename)
            if filepath.exists():
                self.history = pd.read_csv(filepath)
            else:
                # If file doesn't exist, start with empty history
                self.history = pd.DataFrame(columns=['operation', 'operand_a', 'operand_b', 'result', 'timestamp'])
        except Exception as e:
            raise HistoryError(f"Failed to load history: {e}")
    
    def get_count(self) -> int:
        """Get number of calculations in history."""
        return len(self.history)
    
    # Observer pattern methods
    def attach_observer(self, observer: HistoryObserver):
        """Add an observer."""
        if observer not in self._observers:
            self._observers.append(observer)
            
            # If it's AutoSaveObserver, give it reference to history
            if isinstance(observer, AutoSaveObserver):
                observer.set_history(self)
    
    def detach_observer(self, observer: HistoryObserver):
        """Remove an observer."""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def _notify_observers(self, calculation: Calculation):
        """Notify all observers of a new calculation."""
        for observer in self._observers:
            observer.update(calculation)
    
    def __str__(self) -> str:
        """Return string representation of history."""
        if len(self.history) == 0:
            return "No calculations in history"
        
        result = f"Calculation History ({len(self.history)} calculations):\n"
        result += "-" * 80 + "\n"
        
        for idx, row in self.history.iterrows():
            result += f"{idx + 1}. {row['operand_a']} {self._get_symbol(row['operation'])} {row['operand_b']} = {row['result']} [{row['timestamp']}]\n"
        
        return result
    
    def _get_symbol(self, operation: str) -> str:
        """Get symbol for operation name."""
        symbols = {
            'add': '+',
            'subtract': '-',
            'multiply': '×',
            'divide': '÷',
            'power': '^',
            'root': '√',
            'modulus': '%',
            'int_divide': '//',
            'percent': '%of',
            'abs_diff': '|Δ|'
        }
        return symbols.get(operation, operation)