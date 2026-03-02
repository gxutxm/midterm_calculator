"""Tests for input validators."""

import pytest
from app.input_validators import InputValidator
from app.exceptions import ValidationError


class TestInputValidator:
    def test_validate_number_valid_integer(self):
        validator = InputValidator()
        assert validator.validate_number("5") == 5.0
    
    def test_validate_number_valid_float(self):
        validator = InputValidator()
        assert validator.validate_number("5.5") == 5.5
    
    def test_validate_number_negative(self):
        validator = InputValidator()
        assert validator.validate_number("-10") == -10.0
    
    def test_validate_number_invalid_string(self):
        validator = InputValidator()
        with pytest.raises(ValidationError):
            validator.validate_number("hello")
    
    def test_validate_number_exceeds_max(self):
        validator = InputValidator(max_value=100)
        with pytest.raises(ValidationError):
            validator.validate_number("200")
    
    def test_validate_operation_valid(self):
        validator = InputValidator()
        operations = ['add', 'subtract']
        assert validator.validate_operation('add', operations) == 'add'
    
    def test_validate_operation_case_insensitive(self):
        validator = InputValidator()
        operations = ['add', 'subtract']
        assert validator.validate_operation('ADD', operations) == 'add'
    
    def test_validate_operation_invalid(self):
        validator = InputValidator()
        operations = ['add', 'subtract']
        with pytest.raises(ValidationError):
            validator.validate_operation('multiply', operations)
    
    def test_validate_operation_empty(self):
        validator = InputValidator()
        operations = ['add', 'subtract']
        with pytest.raises(ValidationError):
            validator.validate_operation('', operations)