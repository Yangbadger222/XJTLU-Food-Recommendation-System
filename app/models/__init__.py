"""Models package."""
from .food import FoodItem, NutritionInfo, FoodRecommendation
from .user import User, UserPreferences, FoodHistory, RecommendationRequest, FitnessGoal

__all__ = [
    "FoodItem",
    "NutritionInfo", 
    "FoodRecommendation",
    "User",
    "UserPreferences",
    "FoodHistory",
    "RecommendationRequest",
    "FitnessGoal",
]
