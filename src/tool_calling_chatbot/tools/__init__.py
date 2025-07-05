"""Tools for the chatbot function calling system."""

from .calculator import Calculator
from .file_reader import FileReader
from .random_joke import RandomJoke
from ..core.base import registry

# Register all tools
calculator = Calculator()
file_reader = FileReader()
random_joke = RandomJoke()

registry.register(calculator)
registry.register(file_reader)
registry.register(random_joke)

__all__ = ["Calculator", "FileReader", "RandomJoke", "registry"] 