"""tools for the chatbot function calling system."""

from .calculator import Calculator
from .vintage_outfit_generator import VintageOutfitGenerator
from .narrm_food_recommender import NarrmFoodRecommender
from ..core.base import registry

# register all tools
calculator = Calculator()
vintage_outfit_generator = VintageOutfitGenerator()
narrm_food_recommender = NarrmFoodRecommender()

registry.register(calculator)
registry.register(vintage_outfit_generator)
registry.register(narrm_food_recommender)

__all__ = ["Calculator", "VintageOutfitGenerator", "NarrmFoodRecommender", "registry"] 