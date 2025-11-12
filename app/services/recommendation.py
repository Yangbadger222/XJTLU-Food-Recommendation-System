"""Recommendation service that combines RAG and DeepSeek."""
from typing import List, Optional
import re
from app.models import (
    FoodItem, FoodRecommendation, NutritionInfo,
    UserPreferences, RecommendationRequest
)
from app.services.rag_service import get_rag_service
from app.services.deepseek_service import get_deepseek_service
from app.database import get_user_db


class RecommendationService:
    """推荐服务，整合RAG和AI生成."""
    
    def __init__(self):
        """Initialize recommendation service."""
        self.rag_service = get_rag_service()
        self.deepseek_service = get_deepseek_service()
    
    async def _get_user_history_summary(self, user_id: str) -> List[str]:
        """获取用户历史摘要."""
        user_db = await get_user_db()
        history = await user_db.get_user_history(user_id, limit=20)
        
        return [
            f"{h.food_name} ({h.canteen}) - {h.meal_type} - 评分: {h.rating or '未评分'}"
            for h in history
        ]
    
    def _parse_ai_response(
        self,
        ai_response: str,
        available_foods: List[FoodItem]
    ) -> tuple[List[FoodItem], str, str]:
        """解析AI响应，提取推荐的食物."""
        recommended_foods = []
        
        # Create food name to object mapping
        food_map = {food.name: food for food in available_foods}
        
        # Extract food names from response
        # Look for patterns like "1. 鸡胸肉沙拉 - 食堂一"
        food_pattern = r'\d+\.\s*([^-\n]+?)\s*-'
        matches = re.findall(food_pattern, ai_response)
        
        for match in matches:
            food_name = match.strip()
            # Try to find matching food
            for fname, food in food_map.items():
                if food_name in fname or fname in food_name:
                    if food not in recommended_foods:
                        recommended_foods.append(food)
                    break
        
        # Extract reasoning and tips
        reasoning = ""
        tips = ""
        
        # Extract reasoning section
        reasoning_match = re.search(
            r'\*\*推荐理由[：:]\*\*\s*(.+?)(?=\*\*|$)',
            ai_response,
            re.DOTALL
        )
        if reasoning_match:
            reasoning = reasoning_match.group(1).strip()
        
        # Extract tips section
        tips_match = re.search(
            r'\*\*饮食建议[：:]\*\*\s*(.+?)(?=\*\*|$)',
            ai_response,
            re.DOTALL
        )
        if tips_match:
            tips = tips_match.group(1).strip()
        
        return recommended_foods, reasoning or ai_response, tips
    
    def _calculate_total_nutrition(self, foods: List[FoodItem]) -> NutritionInfo:
        """计算总营养."""
        total_calories = sum(f.nutrition.calories for f in foods)
        total_protein = sum(f.nutrition.protein for f in foods)
        total_carbs = sum(f.nutrition.carbs for f in foods)
        total_fat = sum(f.nutrition.fat for f in foods)
        total_fiber = sum(f.nutrition.fiber or 0 for f in foods)
        total_sodium = sum(f.nutrition.sodium or 0 for f in foods)
        
        return NutritionInfo(
            calories=round(total_calories, 1),
            protein=round(total_protein, 1),
            carbs=round(total_carbs, 1),
            fat=round(total_fat, 1),
            fiber=round(total_fiber, 1) if total_fiber > 0 else None,
            sodium=round(total_sodium, 1) if total_sodium > 0 else None
        )
    
    async def get_recommendation(
        self,
        request: RecommendationRequest
    ) -> FoodRecommendation:
        """获取食物推荐."""
        
        # Get user data
        user_db = await get_user_db()
        user = await user_db.get_user(request.user_id)
        
        # Use request preferences or user's saved preferences
        preferences = request.preferences
        if not preferences and user and user.preferences:
            preferences = user.preferences
        
        # Get user history for context
        history_summary = await self._get_user_history_summary(request.user_id)
        
        # Retrieve relevant foods using RAG
        relevant_foods = await self.rag_service.retrieve_relevant_foods(
            meal_type=request.meal_type,
            preferences=preferences,
            custom_requirements=request.custom_requirements,
            n_results=15
        )
        
        if not relevant_foods:
            # Fallback: return empty recommendation
            return FoodRecommendation(
                food_items=[],
                total_nutrition=NutritionInfo(
                    calories=0, protein=0, carbs=0, fat=0
                ),
                reasoning="抱歉，没有找到符合要求的食物。",
                tips="请尝试调整您的偏好设置或选择其他餐次。"
            )
        
        # Generate recommendation using DeepSeek
        ai_response = await self.deepseek_service.generate_recommendation(
            available_foods=relevant_foods,
            preferences=preferences,
            meal_type=request.meal_type,
            recent_history=history_summary,
            custom_requirements=request.custom_requirements
        )
        
        # Parse AI response
        recommended_foods, reasoning, tips = self._parse_ai_response(
            ai_response, relevant_foods
        )
        
        # If parsing failed, use top foods from RAG
        if not recommended_foods:
            recommended_foods = relevant_foods[:3]
            reasoning = ai_response
        
        # Calculate total nutrition
        total_nutrition = self._calculate_total_nutrition(recommended_foods)
        
        return FoodRecommendation(
            food_items=recommended_foods,
            total_nutrition=total_nutrition,
            reasoning=reasoning,
            tips=tips or None
        )


# Global instance
_recommendation_service: Optional[RecommendationService] = None


def get_recommendation_service() -> RecommendationService:
    """获取推荐服务单例."""
    global _recommendation_service
    if _recommendation_service is None:
        _recommendation_service = RecommendationService()
    return _recommendation_service
