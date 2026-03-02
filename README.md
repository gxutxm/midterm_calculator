# Advanced Calculator - Midterm Project

A command-line calculator with 10 operations, undo/redo, logging, history management, and colored output.

## Features

- 10 arithmetic operations: add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff
- Undo and redo functionality (Memento pattern)
- Calculation history with pandas DataFrames
- Auto-save to CSV files
- File logging with Python logging module
- Observer pattern for logging and auto-save
- Configuration management with environment variables
- Colored terminal output with Colorama
- 95% test coverage with 147 tests

## Installation
```bash
# Clone repository
git clone https://github.com/YOUR-USERNAME/calculator-midterm.git
cd calculator-midterm

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

The `.env` file contains configuration settings:
```
CALCULATOR_LOG_DIR=logs/
CALCULATOR_HISTORY_DIR=history/
CALCULATOR_MAX_HISTORY_SIZE=1000
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=2
CALCULATOR_MAX_INPUT_VALUE=1000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```

## Usage
```bash
# Run calculator
python -m app.calculator
```

### Available Operations

- add - Addition
- subtract - Subtraction
- multiply - Multiplication
- divide - Division
- power - Exponentiation (a^b)
- root - Nth root (b-th root of a)
- modulus - Remainder (a % b)
- int_divide - Integer division (a // b)
- percent - Percentage ((a/b)*100)
- abs_diff - Absolute difference (|a-b|)

### Available Commands

- help - Show help message
- history - View calculation history
- clear - Clear history
- undo - Undo last calculation
- redo - Redo last undone calculation
- save - Save history to CSV
- load - Load history from CSV
- exit - Exit calculator

## Project Structure
```
calculator-midterm/
├── app/
│   ├── calculator.py          # Main REPL interface
│   ├── calculation.py         # Calculation class
│   ├── calculator_config.py   # Configuration management
│   ├── calculator_memento.py  # Undo/redo functionality
│   ├── exceptions.py          # Custom exceptions
│   ├── history.py             # History with Observer pattern
│   ├── input_validators.py    # Input validation
│   ├── operations.py          # 10 operations with Strategy pattern
│   └── logger.py              # Logging module
├── tests/                     # 147 comprehensive tests
├── logs/                      # Log files
├── history/                   # CSV history files
├── .env                       # Configuration
├── requirements.txt
└── README.md
```

## Design Patterns

### Factory Pattern
`OperationFactory` creates operation instances dynamically.

### Strategy Pattern
Each operation is a separate strategy class that can be swapped at runtime.

### Observer Pattern
`LoggingObserver` and `AutoSaveObserver` respond to calculation events.

### Memento Pattern
`CalculatorMemento` and `CalculatorCaretaker` enable undo/redo functionality.

### Facade Pattern
`Calculator` class provides simple interface to complex subsystems.

## Testing
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Check coverage (95%)
pytest --cov=app tests/ --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=app --cov-report=html
```

**Test Results:**
- 147 tests pass
- 95% code coverage

## Error Handling

### LBYL (Look Before You Leap)
Used in division operations - checks for zero before dividing.

### EAFP (Easier to Ask Forgiveness than Permission)
Used in calculation execution - attempts operation and handles exceptions.

## Logging

All calculations, errors, and events are logged to files in the `logs/` directory with timestamps and appropriate logging levels.

## Optional Feature: Colorama

The calculator uses Colorama for colored terminal output:
- Green for successful results
- Red for errors
- Cyan for headers
- Yellow for commands

## CI/CD

GitHub Actions automatically runs tests and checks coverage on every push.

## Requirements

- Python 3.8+
- pandas 2.1.4+
- python-dotenv 1.0.0+
- colorama 0.4.6+
- pytest 7.4.3+
- pytest-cov 4.1.0+

