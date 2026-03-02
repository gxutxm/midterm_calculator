"""Memento pattern for undo/redo functionality."""

from typing import List, Optional
import pandas as pd
from app.exceptions import MementoError


class CalculatorMemento:
    """
    Stores a snapshot of calculator state.
    
    Memento pattern - saves state for undo/redo.
    """
    
    def __init__(self, history_data: pd.DataFrame):
        """
        Create a memento with current state.
        
        Args:
            history_data: DataFrame containing history
        """
        self._history_data = history_data.copy()
    
    def get_state(self) -> pd.DataFrame:
        """Get the saved state."""
        return self._history_data.copy()


class CalculatorCaretaker:
    """
    Manages mementos for undo/redo.
    
    Keeps track of history states.
    """
    
    def __init__(self):
        """Create empty undo/redo stacks."""
        self._undo_stack: List[CalculatorMemento] = []
        self._redo_stack: List[CalculatorMemento] = []
    
    def save(self, memento: CalculatorMemento):
        """
        Save current state.
        
        Args:
            memento: State to save
        """
        self._undo_stack.append(memento)
        # Clear redo stack when new action is performed
        self._redo_stack.clear()
    
    def undo(self) -> CalculatorMemento:
        """
        Undo to previous state.
        
        Returns:
            Previous state
            
        Raises:
            MementoError: If nothing to undo
        """
        if not self.can_undo():
            raise MementoError("Nothing to undo")
        
        # Move current state to redo stack
        current = self._undo_stack.pop()
        self._redo_stack.append(current)
        
        # Return previous state
        if len(self._undo_stack) > 0:
            return self._undo_stack[-1]
        else:
            # No more states, return empty state
            import pandas as pd
            return CalculatorMemento(pd.DataFrame(columns=['operation', 'operand_a', 'operand_b', 'result', 'timestamp']))
    
    def redo(self) -> CalculatorMemento:
        """
        Redo to next state.
        
        Returns:
            Next state
            
        Raises:
            MementoError: If nothing to redo
        """
        if not self.can_redo():
            raise MementoError("Nothing to redo")
        
        # Move state back to undo stack
        state = self._redo_stack.pop()
        self._undo_stack.append(state)
        
        return state
    
    def can_undo(self) -> bool:
        """Check if undo is available."""
        return len(self._undo_stack) > 1
    
    def can_redo(self) -> bool:
        """Check if redo is available."""
        return len(self._redo_stack) > 0
    
    def clear(self):
        """Clear all saved states."""
        self._undo_stack.clear()
        self._redo_stack.clear()
    
    def get_undo_count(self) -> int:
        """Get number of undo operations available."""
        return max(0, len(self._undo_stack) - 1)
    
    def get_redo_count(self) -> int:
        """Get number of redo operations available."""
        return len(self._redo_stack)