"""tools for the chatbot function calling system."""

from .calculator import Calculator
from .vintage_outfit_generator import VintageOutfitGenerator
from .melbourne_food_recommender import MelbourneFoodRecommender
from ..core.base import registry

# register all tools
calculator = Calculator()
vintage_outfit_generator = VintageOutfitGenerator()
melbourne_food_recommender = MelbourneFoodRecommender()

registry.register(calculator)
registry.register(vintage_outfit_generator)
registry.register(melbourne_food_recommender)

__all__ = ["Calculator", "VintageOutfitGenerator", "MelbourneFoodRecommender", "registry"] 