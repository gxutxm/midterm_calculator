"""Tests for operations."""

import pytest
from app.operations import (
    AddOperation, SubtractOperation, MultiplyOperation, DivideOperation,
    PowerOperation, RootOperation, ModulusOperation, IntDivideOperation,
    PercentOperation, AbsDiffOperation, OperationFactory
)
from app.exceptions import DivisionByZeroError, OperationError


class TestAddOperation:
    def test_add_positive(self):
        op = AddOperation()
        assert op.execute(5, 3) == 8
    
    def test_add_negative(self):
        op = AddOperation()
        assert op.execute(-5, -3) == -8
    
    def test_symbol(self):
        op = AddOperation()
        assert op.symbol == "+"


class TestSubtractOperation:
    def test_subtract(self):
        op = SubtractOperation()
        assert op.execute(10, 3) == 7
    
    def test_symbol(self):
        op = SubtractOperation()
        assert op.symbol == "-"


class TestMultiplyOperation:
    def test_multiply(self):
        op = MultiplyOperation()
        assert op.execute(4, 5) == 20
    
    def test_symbol(self):
        op = MultiplyOperation()
        assert op.symbol == "×"


class TestDivideOperation:
    def test_divide(self):
        op = DivideOperation()
        assert op.execute(10, 2) == 5
    
    def test_divide_by_zero(self):
        op = DivideOperation()
        with pytest.raises(DivisionByZeroError):
            op.execute(10, 0)
    
    def test_symbol(self):
        op = DivideOperation()
        assert op.symbol == "÷"


class TestPowerOperation:
    def test_power(self):
        op = PowerOperation()
        assert op.execute(2, 3) == 8
    
    def test_symbol(self):
        op = PowerOperation()
        assert op.symbol == "^"


class TestRootOperation:
    def test_square_root(self):
        op = RootOperation()
        assert op.execute(9, 2) == 3
    
    def test_root_zero_raises_error(self):
        op = RootOperation()
        with pytest.raises(DivisionByZeroError):
            op.execute(9, 0)
    
    def test_negative_even_root_raises_error(self):
        op = RootOperation()
        with pytest.raises(OperationError):
            op.execute(-9, 2)
    
    def test_symbol(self):
        op = RootOperation()
        assert op.symbol == "√"


class TestModulusOperation:
    def test_modulus(self):
        op = ModulusOperation()
        assert op.execute(10, 3) == 1
    
    def test_modulus_zero_raises_error(self):
        op = ModulusOperation()
        with pytest.raises(DivisionByZeroError):
            op.execute(10, 0)
    
    def test_symbol(self):
        op = ModulusOperation()
        assert op.symbol == "%"


class TestIntDivideOperation:
    def test_int_divide(self):
        op = IntDivideOperation()
        assert op.execute(10, 3) == 3
    
    def test_int_divide_zero_raises_error(self):
        op = IntDivideOperation()
        with pytest.raises(DivisionByZeroError):
            op.execute(10, 0)
    
    def test_symbol(self):
        op = IntDivideOperation()
        assert op.symbol == "//"


class TestPercentOperation:
    def test_percent(self):
        op = PercentOperation()
        assert op.execute(100, 10) == 1000
    
    def test_percent_zero_raises_error(self):
        op = PercentOperation()
        with pytest.raises(DivisionByZeroError):
            op.execute(50, 0)
    
    def test_symbol(self):
        op = PercentOperation()
        assert op.symbol == "%of"


class TestAbsDiffOperation:
    def test_abs_diff_positive(self):
        op = AbsDiffOperation()
        assert op.execute(10, 3) == 7
    
    def test_abs_diff_negative(self):
        op = AbsDiffOperation()
        assert op.execute(3, 10) == 7
    
    def test_symbol(self):
        op = AbsDiffOperation()
        assert op.symbol == "|Δ|"


class TestOperationFactory:
    def test_create_all_operations(self):
        """Test creating all 10 operations."""
        operations = ['add', 'subtract', 'multiply', 'divide', 'power', 
                     'root', 'modulus', 'int_divide', 'percent', 'abs_diff']
        
        for op_name in operations:
            op = OperationFactory.create_operation(op_name)
            assert op is not None
    
    def test_unknown_operation_raises_error(self):
        with pytest.raises(OperationError):
            OperationFactory.create_operation('unknown')
    
    def test_get_available_operations(self):
        ops = OperationFactory.get_available_operations()
        assert len(ops) == 10
        assert 'add' in ops
        assert 'modulus' in ops


@pytest.mark.parametrize("operation,a,b,expected", [
    ('add', 5, 3, 8),
    ('subtract', 10, 3, 7),
    ('multiply', 4, 5, 20),
    ('divide', 10, 2, 5),
    ('power', 2, 3, 8),
    ('modulus', 10, 3, 1),
    ('int_divide', 10, 3, 3),
    ('abs_diff', 3, 10, 7),
])
def test_operations_parameterized(operation, a, b, expected):
    """Test multiple operations with parameters."""
    op = OperationFactory.create_operation(operation)
    assert op.execute(a, b) == expected