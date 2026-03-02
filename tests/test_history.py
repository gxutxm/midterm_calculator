"""Tests for calculation history."""

import pytest
import pandas as pd
from pathlib import Path
from app.history import CalculationHistory, LoggingObserver, AutoSaveObserver
from app.calculation import Calculation
from app.exceptions import HistoryError


class TestCalculationHistory:
    def test_history_initializes_empty(self):
        history = CalculationHistory()
        assert len(history.history) == 0
        assert history.get_count() == 0
    
    def test_add_calculation(self):
        history = CalculationHistory()
        calc = Calculation('add', 5, 3)
        calc.execute()
        history.add_calculation(calc)
        assert history.get_count() == 1
    
    def test_get_all_returns_dataframe(self):
        history = CalculationHistory()
        calc = Calculation('add', 5, 3)
        calc.execute()
        history.add_calculation(calc)
        df = history.get_all()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
    
    def test_get_last_calculation(self):
        history = CalculationHistory()
        calc1 = Calculation('add', 5, 3)
        calc1.execute()
        calc2 = Calculation('multiply', 4, 5)
        calc2.execute()
        history.add_calculation(calc1)
        history.add_calculation(calc2)
        last = history.get_last()
        assert last['operation'] == 'multiply'
    
    def test_get_last_empty_history_raises_error(self):
        history = CalculationHistory()
        with pytest.raises(HistoryError):
            history.get_last()
    
    def test_clear_history(self):
        history = CalculationHistory()
        calc = Calculation('add', 5, 3)
        calc.execute()
        history.add_calculation(calc)
        assert history.get_count() == 1
        history.clear()
        assert history.get_count() == 0
    
    def test_save_to_csv(self, tmp_path):
        history = CalculationHistory()
        calc = Calculation('add', 5, 3)
        calc.execute()
        history.add_calculation(calc)
        
        filename = tmp_path / "test_history.csv"
        history.save_to_csv(str(filename))
        assert filename.exists()
    
    def test_load_from_csv(self, tmp_path):
        history = CalculationHistory()
        calc = Calculation('add', 5, 3)
        calc.execute()
        history.add_calculation(calc)
        
        filename = tmp_path / "test_history.csv"
        history.save_to_csv(str(filename))
        
        new_history = CalculationHistory()
        new_history.load_from_csv(str(filename))
        assert new_history.get_count() == 1
    
    def test_load_nonexistent_file(self):
        history = CalculationHistory()
        history.load_from_csv("nonexistent.csv")
        assert history.get_count() == 0
    
    def test_history_str_empty(self):
        history = CalculationHistory()
        assert "No calculations" in str(history)
    
    def test_history_str_with_calculations(self):
        history = CalculationHistory()
        calc = Calculation('add', 5, 3)
        calc.execute()
        history.add_calculation(calc)
        history_str = str(history)
        assert "Calculation History" in history_str
    
    def test_attach_observer(self):
        history = CalculationHistory()
        observer = LoggingObserver()
        history.attach_observer(observer)
        assert observer in history._observers
    
    def test_detach_observer(self):
        history = CalculationHistory()
        observer = LoggingObserver()
        history.attach_observer(observer)
        history.detach_observer(observer)
        assert observer not in history._observers
    
    def test_max_history_size(self):
        history = CalculationHistory(max_size=3)
        for i in range(5):
            calc = Calculation('add', i, 1)
            calc.execute()
            history.add_calculation(calc)
        assert history.get_count() == 3


class TestAutoSaveObserver:
    def test_auto_save_observer(self, tmp_path):
        filename = tmp_path / "auto_save.csv"
        observer = AutoSaveObserver(filename)
        history = CalculationHistory()
        observer.set_history(history)
        history.attach_observer(observer)
        
        calc = Calculation('add', 5, 3)
        calc.execute()
        history.add_calculation(calc)
        
        assert filename.exists()