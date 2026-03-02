"""Main calculator REPL interface with colored output."""

from colorama import Fore, Style, init
from app.calculation import Calculation
from app.history import CalculationHistory, LoggingObserver, AutoSaveObserver
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento, CalculatorCaretaker
from app.input_validators import InputValidator
from app.operations import OperationFactory
from app.logger import get_logger
from app.exceptions import (
    CalculatorError, ValidationError, OperationError,
    DivisionByZeroError, HistoryError, MementoError
)


# Initialize colorama
init(autoreset=True)


class Calculator:
    """
    Main calculator with REPL interface.
    
    Implements Facade pattern - simple interface to complex subsystems.
    Uses Colorama for colored output.
    """
    
    def __init__(self):
        """Initialize calculator with all components."""
        # Load configuration
        self.config = CalculatorConfig()
        
        # Initialize logger
        self.logger = get_logger(str(self.config.log_dir), "INFO")
        self.logger.log_info("Calculator started")
        
        # Initialize validator
        self.validator = InputValidator(self.config.max_input_value)
        
        # Initialize history
        self.history = CalculationHistory(self.config.max_history_size)
        
        # Load existing history
        try:
            self.history.load_from_csv(str(self.config.history_file))
            self.logger.log_info(f"Loaded {self.history.get_count()} calculations from history")
        except Exception as e:
            self.logger.log_warning(f"Could not load history: {e}")
        
        # Set up observers
        logging_observer = LoggingObserver(str(self.config.log_dir))
        self.history.attach_observer(logging_observer)
        
        if self.config.auto_save:
            auto_save_observer = AutoSaveObserver(self.config.history_file)
            self.history.attach_observer(auto_save_observer)
        
        # Initialize memento for undo/redo
        self.caretaker = CalculatorCaretaker()
        self._save_state()
        
        # Get available operations
        self.available_operations = OperationFactory.get_available_operations()
        
        # Define commands
        self.commands = ['help', 'history', 'exit', 'quit', 'clear', 'undo', 'redo', 'save', 'load']
        
        self.running = False
    
    def _save_state(self):
        """Save current state for undo/redo."""
        memento = CalculatorMemento(self.history.history)
        self.caretaker.save(memento)
    
    def _restore_state(self, memento: CalculatorMemento):
        """Restore state from memento."""
        self.history.history = memento.get_state()
    
    def display_welcome(self):
        """Show welcome message with colors."""
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.CYAN + "ADVANCED CALCULATOR v1.0")
        print(Fore.CYAN + "=" * 80)
        print(Fore.GREEN + "\nAvailable operations:")
        for op in self.available_operations:
            print(Fore.GREEN + f"  • {op}")
        print(Fore.YELLOW + "\nCommands:")
        print(Fore.YELLOW + "  • help    - Show this help")
        print(Fore.YELLOW + "  • history - View calculation history")
        print(Fore.YELLOW + "  • clear   - Clear history")
        print(Fore.YELLOW + "  • undo    - Undo last calculation")
        print(Fore.YELLOW + "  • redo    - Redo last undone calculation")
        print(Fore.YELLOW + "  • save    - Save history to CSV")
        print(Fore.YELLOW + "  • load    - Load history from CSV")
        print(Fore.YELLOW + "  • exit    - Exit calculator")
        print(Fore.CYAN + "=" * 80 + "\n")
    
    def display_help(self):
        """Show help message."""
        print(Fore.CYAN + "\n" + "-" * 80)
        print(Fore.CYAN + "HELP")
        print(Fore.CYAN + "-" + "-" * 80)
        print("\nTo perform a calculation:")
        print("  1. Enter operation name")
        print("  2. Enter first number")
        print("  3. Enter second number")
        print(Fore.GREEN + "\nAvailable operations:", ', '.join(self.available_operations))
        print(Fore.YELLOW + "Available commands:", ', '.join(self.commands))
        print(Fore.CYAN + "-" * 80 + "\n")
    
    def display_history(self):
        """Show calculation history."""
        print(Fore.CYAN + "\n" + str(self.history))
    
    def get_input(self, prompt: str) -> str:
        """Get user input with prompt."""
        return input(prompt).strip()
    
    def perform_calculation(self, operation: str):
        """Execute a calculation."""
        try:
            # Get operands
            a_str = self.get_input("Enter first number: ")
            a = self.validator.validate_number(a_str)
            
            b_str = self.get_input("Enter second number: ")
            b = self.validator.validate_number(b_str)
            
            # Create and execute calculation
            calc = Calculation(operation, a, b)
            result = calc.execute()
            
            # Round result based on precision
            result = round(result, self.config.precision)
            calc._result = result
            
            # Add to history
            self.history.add_calculation(calc)
            
            # Save state for undo
            self._save_state()
            
            # Display result with color
            print(Fore.GREEN + f"\nResult: {calc}\n")
            
        except (ValidationError, OperationError, DivisionByZeroError) as e:
            print(Fore.RED + f"\nError: {e}\n")
            self.logger.log_error(str(e))
        except Exception as e:
            print(Fore.RED + f"\nUnexpected error: {e}\n")
            self.logger.log_error(f"Unexpected error: {e}")
    
    def handle_command(self, command: str) -> bool:
        """
        Handle a command.
        
        Returns:
            True if should continue, False if should exit
        """
        if command in ['exit', 'quit']:
            return False
        
        elif command == 'help':
            self.display_help()
        
        elif command == 'history':
            self.display_history()
        
        elif command == 'clear':
            self.history.clear()
            self._save_state()
            print(Fore.GREEN + "\nHistory cleared.\n")
            self.logger.log_info("History cleared")
        
        elif command == 'undo':
            try:
                memento = self.caretaker.undo()
                self._restore_state(memento)
                print(Fore.GREEN + f"\nUndo successful. ({self.caretaker.get_undo_count()} more available)\n")
                self.logger.log_info("Undo performed")
            except MementoError as e:
                print(Fore.RED + f"\n{e}\n")
        
        elif command == 'redo':
            try:
                memento = self.caretaker.redo()
                self._restore_state(memento)
                print(Fore.GREEN + f"\nRedo successful. ({self.caretaker.get_redo_count()} more available)\n")
                self.logger.log_info("Redo performed")
            except MementoError as e:
                print(Fore.RED + f"\n{e}\n")
        
        elif command == 'save':
            self.history.save_to_csv(str(self.config.history_file))
            print(Fore.GREEN + f"\nHistory saved to {self.config.history_file}\n")
            self.logger.log_info("History saved manually")
        
        elif command == 'load':
            self.history.load_from_csv(str(self.config.history_file))
            self._save_state()
            print(Fore.GREEN + f"\nHistory loaded from {self.config.history_file}\n")
            self.logger.log_info("History loaded")
        
        return True
    
    def run(self):
        """Start the calculator REPL."""
        self.running = True
        self.display_welcome()
        
        try:
            while self.running:
                user_input = self.get_input(Fore.WHITE + "Enter operation or command: ").lower()
                
                if not user_input:
                    continue
                
                # Check if it's a command
                if user_input in self.commands:
                    should_continue = self.handle_command(user_input)
                    if not should_continue:
                        print(Fore.CYAN + "\nThank you for using the calculator. Goodbye!\n")
                        self.logger.log_info("Calculator closed")
                        break
                
                # Check if it's an operation
                elif user_input in self.available_operations:
                    self.perform_calculation(user_input)
                
                else:
                    print(Fore.RED + f"\nUnknown input: '{user_input}'. Type 'help' for instructions.\n")
        
        except KeyboardInterrupt:
            print(Fore.CYAN + "\n\nCalculator interrupted. Goodbye!\n")
            self.logger.log_info("Calculator interrupted")
        except Exception as e:  # pragma: no cover
            print(Fore.RED + f"\nFatal error: {e}\n")
            self.logger.log_error(f"Fatal error: {e}")


def main():  # pragma: no cover
    """Entry point for the calculator."""
    calculator = Calculator()
    calculator.run()


if __name__ == "__main__":  # pragma: no cover
    main()