"""Tests for Calculator REPL."""

import pytest
from unittest.mock import patch, MagicMock
from app.calculator import Calculator
from app.exceptions import ValidationError


class TestCalculator:
    def test_calculator_initialization(self):
        calc = Calculator()
        assert calc.config is not None
        assert calc.history is not None
        assert calc.caretaker is not None
        assert not calc.running
    
    def test_display_welcome(self, capsys):
        calc = Calculator()
        calc.display_welcome()
        captured = capsys.readouterr()
        assert "ADVANCED CALCULATOR" in captured.out
        assert "operations:" in captured.out.lower()
    
    def test_display_help(self, capsys):
        calc = Calculator()
        calc.display_help()
        captured = capsys.readouterr()
        assert "HELP" in captured.out
    
    def test_display_history(self, capsys):
        calc = Calculator()
        calc.display_history()
        captured = capsys.readouterr()
        assert "calculations" in captured.out.lower() or "history" in captured.out.lower()
    
    @patch('builtins.input', return_value='5')
    def test_get_input(self, mock_input):
        calc = Calculator()
        result = calc.get_input("Test: ")
        assert result == '5'
    
    @patch('builtins.input', side_effect=['5', '3'])
    def test_perform_calculation_add(self, mock_input, capsys):
        calc = Calculator()
        calc.perform_calculation('add')
        captured = capsys.readouterr()
        assert "Result:" in captured.out
        assert "8" in captured.out
    
    @patch('builtins.input', side_effect=['10', '2'])
    def test_perform_calculation_divide(self, mock_input, capsys):
        calc = Calculator()
        calc.perform_calculation('divide')
        captured = capsys.readouterr()
        assert "5" in captured.out
    
    @patch('builtins.input', side_effect=['10', '0'])
    def test_perform_calculation_division_by_zero(self, mock_input, capsys):
        calc = Calculator()
        calc.perform_calculation('divide')
        captured = capsys.readouterr()
        assert "Error:" in captured.out
    
    @patch('builtins.input', side_effect=['abc', '5'])
    def test_perform_calculation_invalid_input(self, mock_input, capsys):
        calc = Calculator()
        calc.perform_calculation('add')
        captured = capsys.readouterr()
        assert "Error:" in captured.out
    
    def test_handle_command_exit(self):
        calc = Calculator()
        result = calc.handle_command('exit')
        assert result is False
    
    def test_handle_command_quit(self):
        calc = Calculator()
        result = calc.handle_command('quit')
        assert result is False
    
    def test_handle_command_help(self, capsys):
        calc = Calculator()
        result = calc.handle_command('help')
        assert result is True
        captured = capsys.readouterr()
        assert "HELP" in captured.out
    
    def test_handle_command_history(self, capsys):
        calc = Calculator()
        result = calc.handle_command('history')
        assert result is True
    
    def test_handle_command_clear(self, capsys):
        calc = Calculator()
        result = calc.handle_command('clear')
        assert result is True
        assert calc.history.get_count() == 0
    
    def test_handle_command_undo_no_history(self, capsys):
        calc = Calculator()
        result = calc.handle_command('undo')
        assert result is True
        captured = capsys.readouterr()
        assert "Nothing to undo" in captured.out or "Error" in captured.out
    
    def test_handle_command_redo_no_history(self, capsys):
        calc = Calculator()
        result = calc.handle_command('redo')
        assert result is True
        captured = capsys.readouterr()
        assert "Nothing to redo" in captured.out or "Error" in captured.out
    
    def test_handle_command_save(self, capsys, tmp_path):
        calc = Calculator()
        calc.config.history_file = tmp_path / "test.csv"
        result = calc.handle_command('save')
        assert result is True
    
    def test_handle_command_load(self, capsys):
        calc = Calculator()
        result = calc.handle_command('load')
        assert result is True
    
    @patch('builtins.input', side_effect=['add', '5', '3', 'exit'])
    def test_run_single_calculation(self, mock_input, capsys):
        calc = Calculator()
        calc.run()
        captured = capsys.readouterr()
        assert "ADVANCED CALCULATOR" in captured.out
        assert "Goodbye" in captured.out
    
    @patch('builtins.input', side_effect=['exit'])
    def test_run_immediate_exit(self, mock_input, capsys):
        calc = Calculator()
        calc.run()
        captured = capsys.readouterr()
        assert "Goodbye" in captured.out
    
    @patch('builtins.input', side_effect=['help', 'exit'])
    def test_run_help_command(self, mock_input, capsys):
        calc = Calculator()
        calc.run()
        captured = capsys.readouterr()
        assert "HELP" in captured.out
    
    @patch('builtins.input', side_effect=['invalid', 'exit'])
    def test_run_invalid_input(self, mock_input, capsys):
        calc = Calculator()
        calc.run()
        captured = capsys.readouterr()
        assert "Unknown input" in captured.out
    
    @patch('builtins.input', side_effect=['', 'exit'])
    def test_run_empty_input(self, mock_input, capsys):
        calc = Calculator()
        calc.run()
        captured = capsys.readouterr()
        assert "Goodbye" in captured.out
    
    @patch('builtins.input', side_effect=KeyboardInterrupt())
    def test_run_keyboard_interrupt(self, mock_input, capsys):
        calc = Calculator()
        calc.run()
        captured = capsys.readouterr()
        assert "interrupted" in captured.out.lower() or "Goodbye" in captured.out
    
    @patch('builtins.input', side_effect=['modulus', '10', '3', 'exit'])
    def test_run_modulus_operation(self, mock_input, capsys):
        calc = Calculator()
        calc.run()
        captured = capsys.readouterr()
        assert "1" in captured.out
    
    @patch('builtins.input', side_effect=['int_divide', '10', '3', 'exit'])
    def test_run_int_divide_operation(self, mock_input, capsys):
        calc = Calculator()
        calc.run()
        captured = capsys.readouterr()
        assert "3" in captured.out
    
    @patch('builtins.input', side_effect=['abs_diff', '3', '10', 'exit'])
    def test_run_abs_diff_operation(self, mock_input, capsys):
        calc = Calculator()
        calc.run()
        captured = capsys.readouterr()
        assert "7" in captured.out