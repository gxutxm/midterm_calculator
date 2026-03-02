"""Tests for Calculation class."""

import pytest
from datetime import datetime
from app.calculation import Calculation
from app.exceptions import OperationError, DivisionByZeroError


class TestCalculation:
    def test_calculation_initialization(self):
        calc = Calculation('add', 5, 3)
        assert calc.operation_name == 'add'
        assert calc.operand_a == 5
        assert calc.operand_b == 3
        assert calc.get_result() is None
        assert isinstance(calc.timestamp, datetime)
    
    def test_calculation_execute_add(self):
        calc = Calculation('add', 5, 3)
        result = calc.execute()
        assert result == 8
        assert calc.get_result() == 8
    
    def test_calculation_execute_subtract(self):
        calc = Calculation('subtract', 10, 4)
        result = calc.execute()
        assert result == 6
    
    def test_calculation_execute_multiply(self):
        calc = Calculation('multiply', 3, 7)
        result = calc.execute()
        assert result == 21
    
    def test_calculation_execute_divide(self):
        calc = Calculation('divide', 20, 4)
        result = calc.execute()
        assert result == 5
    
    def test_calculation_execute_power(self):
        calc = Calculation('power', 2, 3)
        result = calc.execute()
        assert result == 8
    
    def test_calculation_execute_modulus(self):
        calc = Calculation('modulus', 10, 3)
        result = calc.execute()
        assert result == 1
    
    def test_calculation_execute_int_divide(self):
        calc = Calculation('int_divide', 10, 3)
        result = calc.execute()
        assert result == 3
    
    def test_calculation_execute_percent(self):
        calc = Calculation('percent', 100, 10)
        result = calc.execute()
        assert result == 1000
    
    def test_calculation_execute_abs_diff(self):
        calc = Calculation('abs_diff', 3, 10)
        result = calc.execute()
        assert result == 7
    
    def test_calculation_division_by_zero(self):
        calc = Calculation('divide', 10, 0)
        with pytest.raises(OperationError):
            calc.execute()
    
    def test_calculation_invalid_operation(self):
        with pytest.raises(OperationError):
            Calculation('invalid', 5, 3)
    
    def test_calculation_to_dict(self):
        calc = Calculation('add', 5, 3)
        calc.execute()
        result_dict = calc.to_dict()
        assert result_dict['operation'] == 'add'
        assert result_dict['operand_a'] == 5
        assert result_dict['operand_b'] == 3
        assert result_dict['result'] == 8
        assert 'timestamp' in result_dict
    
    def test_calculation_from_dict(self):
        data = {
            'operation': 'multiply',
            'operand_a': 4,
            'operand_b': 5,
            'result': 20,
            'timestamp': '2024-01-01 12:00:00'
        }
        calc = Calculation.from_dict(data)
        assert calc.operation_name == 'multiply'
        assert calc.operand_a == 4
        assert calc.operand_b == 5
        assert calc.get_result() == 20
    
    def test_calculation_str_with_result(self):
        calc = Calculation('add', 5, 3)
        calc.execute()
        calc_str = str(calc)
        assert '5' in calc_str
        assert '3' in calc_str
        assert '8' in calc_str
    
    def test_calculation_str_without_result(self):
        calc = Calculation('add', 5, 3)
        calc_str = str(calc)
        assert '5' in calc_str
        assert '3' in calc_str
    
    def test_calculation_repr(self):
        calc = Calculation('multiply', 4, 5)
        assert 'multiply' in repr(calc)
        assert '4' in repr(calc)
        assert '5' in repr(calc)


@pytest.mark.parametrize("operation,a,b,expected", [
    ('add', 5, 3, 8),
    ('subtract', 10, 3, 7),
    ('multiply', 4, 5, 20),
    ('divide', 20, 4, 5),
    ('power', 2, 3, 8),
    ('modulus', 10, 3, 1),
    ('int_divide', 10, 3, 3),
    ('abs_diff', 3, 10, 7),
])
def test_calculation_parameterized(operation, a, b, expected):
    """Test calculations with different operations."""
    calc = Calculation(operation, a, b)
    result = calc.execute()
    assert result == expected