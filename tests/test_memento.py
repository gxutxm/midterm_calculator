"""Tests for Memento pattern."""

import pytest
import pandas as pd
from app.calculator_memento import CalculatorMemento, CalculatorCaretaker
from app.exceptions import MementoError


class TestCalculatorMemento:
    def test_memento_stores_state(self):
        df = pd.DataFrame({'col': [1, 2, 3]})
        memento = CalculatorMemento(df)
        saved_state = memento.get_state()
        assert len(saved_state) == 3
    
    def test_memento_returns_copy(self):
        df = pd.DataFrame({'col': [1, 2, 3]})
        memento = CalculatorMemento(df)
        saved_state = memento.get_state()
        saved_state.loc[0, 'col'] = 999
        original = memento.get_state()
        assert original.loc[0, 'col'] == 1


class TestCalculatorCaretaker:
    def test_caretaker_initializes_empty(self):
        caretaker = CalculatorCaretaker()
        assert not caretaker.can_undo()
        assert not caretaker.can_redo()
    
    def test_save_memento(self):
        caretaker = CalculatorCaretaker()
        df1 = pd.DataFrame({'state': [1]})
        df2 = pd.DataFrame({'state': [2]})
        caretaker.save(CalculatorMemento(df1))
        caretaker.save(CalculatorMemento(df2))
        assert caretaker.can_undo()
    
    def test_undo_operation(self):
        caretaker = CalculatorCaretaker()
        df1 = pd.DataFrame({'state': [1]})
        df2 = pd.DataFrame({'state': [2]})
        caretaker.save(CalculatorMemento(df1))
        caretaker.save(CalculatorMemento(df2))
        
        previous = caretaker.undo()
        assert previous.get_state()['state'][0] == 1
        assert caretaker.can_redo()
    
    def test_redo_operation(self):
        caretaker = CalculatorCaretaker()
        df1 = pd.DataFrame({'state': [1]})
        df2 = pd.DataFrame({'state': [2]})
        caretaker.save(CalculatorMemento(df1))
        caretaker.save(CalculatorMemento(df2))
        
        caretaker.undo()
        restored = caretaker.redo()
        assert restored.get_state()['state'][0] == 2
    
    def test_undo_without_history_raises_error(self):
        caretaker = CalculatorCaretaker()
        with pytest.raises(MementoError):
            caretaker.undo()
    
    def test_redo_without_history_raises_error(self):
        caretaker = CalculatorCaretaker()
        with pytest.raises(MementoError):
            caretaker.redo()
    
    def test_save_clears_redo_stack(self):
        caretaker = CalculatorCaretaker()
        df1 = pd.DataFrame({'state': [1]})
        df2 = pd.DataFrame({'state': [2]})
        df3 = pd.DataFrame({'state': [3]})
        
        caretaker.save(CalculatorMemento(df1))
        caretaker.save(CalculatorMemento(df2))
        caretaker.undo()
        assert caretaker.can_redo()
        
        caretaker.save(CalculatorMemento(df3))
        assert not caretaker.can_redo()
    
    def test_clear_operation(self):
        caretaker = CalculatorCaretaker()
        df = pd.DataFrame({'state': [1]})
        caretaker.save(CalculatorMemento(df))
        caretaker.clear()
        assert not caretaker.can_undo()
        assert not caretaker.can_redo()
    
    def test_get_undo_count(self):
        caretaker = CalculatorCaretaker()
        assert caretaker.get_undo_count() == 0
        caretaker.save(CalculatorMemento(pd.DataFrame({'state': [1]})))
        caretaker.save(CalculatorMemento(pd.DataFrame({'state': [2]})))
        assert caretaker.get_undo_count() == 1
    
    def test_get_redo_count(self):
        caretaker = CalculatorCaretaker()
        caretaker.save(CalculatorMemento(pd.DataFrame({'state': [1]})))
        caretaker.save(CalculatorMemento(pd.DataFrame({'state': [2]})))
        assert caretaker.get_redo_count() == 0
        caretaker.undo()
        assert caretaker.get_redo_count() == 1