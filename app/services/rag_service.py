"""RAG (Retrieval-Augmented Generation) service."""
from typing import List, Optional, Dict
from app.models import FoodItem, UserPreferences
from app.database import get_vector_db


class RAGService:
    """RAG服务，用于检索相关食物数据."""
    
    def __init__(self):
        """Initialize RAG service."""
        self.vector_db = get_vector_db()
    
    def _build_search_query(
        self,
        meal_type: str,
        preferences: Optional[UserPreferences] = None,
        custom_requirements: Optional[str] = None
    ) -> str:
        """构建搜索查询."""
        query_parts = [meal_type]
        
        if preferences:
            # Add goal to query
            query_parts.append(preferences.goal.value)
            
            # Add dietary restrictions
            if preferences.dietary_restrictions:
                query_parts.extend(preferences.dietary_restrictions)
            
            # Add specific nutrition targets
            if preferences.goal == "减脂":
                query_parts.extend(["低卡路里", "高蛋白", "低脂肪"])
            elif preferences.goal == "增肌":
                query_parts.extend(["高蛋白", "高卡路里"])
            elif preferences.goal == "均衡饮食":
                query_parts.extend(["营养均衡", "健康"])
        
        if custom_requirements:
            query_parts.append(custom_requirements)
        
        return " ".join(query_parts)
    
    def _build_filters(
        self,
        meal_type: str,
        preferences: Optional[UserPreferences] = None
    ) -> Optional[Dict]:
        """构建过滤条件."""
        # Note: ChromaDB filters are limited, mainly for metadata filtering
        # Complex filtering will be done post-retrieval
        return None  # For now, we'll do filtering in post-processing
    
    def _post_filter_foods(
        self,
        foods: List[FoodItem],
        meal_type: str,
        preferences: Optional[UserPreferences] = None
    ) -> List[FoodItem]:
        """后处理过滤食物."""
        filtered = []
        
        for food in foods:
            # Check meal availability
            if meal_type not in food.available_meals:
                continue
            
            if preferences:
                # Check allergies
                if preferences.allergies:
                    has_allergen = any(
                        allergen.lower() in ingredient.lower()
                        for allergen in preferences.allergies
                        for ingredient in food.ingredients
                    )
                    if has_allergen:
                        continue
                
                # Check disliked foods
                if preferences.disliked_foods:
                    is_disliked = any(
                        disliked.lower() in food.name.lower()
                        for disliked in preferences.disliked_foods
                    )
                    if is_disliked:
                        continue
                
                # Check preferred canteens
                if preferences.preferred_canteens:
                    if food.canteen not in preferences.preferred_canteens:
                        continue
            
            filtered.append(food)
        
        return filtered
    
    def _rank_foods_by_goal(
        self,
        foods: List[FoodItem],
        preferences: Optional[UserPreferences] = None
    ) -> List[FoodItem]:
        """根据健康目标对食物进行排序."""
        if not preferences:
            return foods
        
        def score_food(food: FoodItem) -> float:
            """给食物评分."""
            score = 0.0
            
            if preferences.goal == "减脂":
                # Prefer low calorie, high protein, low fat
                score += max(0, 500 - food.nutrition.calories) * 0.3
                score += food.nutrition.protein * 2
                score -= food.nutrition.fat * 1.5
            
            elif preferences.goal == "增肌":
                # Prefer high protein, moderate calories
                score += food.nutrition.protein * 3
                score += min(food.nutrition.calories, 800) * 0.2
            
            elif preferences.goal == "均衡饮食":
                # Balanced nutrition
                ideal_protein_ratio = 0.3  # 30% from protein
                ideal_carb_ratio = 0.5      # 50% from carbs
                ideal_fat_ratio = 0.2       # 20% from fat
                
                total_macros = (
                    food.nutrition.protein * 4 +
                    food.nutrition.carbs * 4 +
                    food.nutrition.fat * 9
                )
                
                if total_macros > 0:
                    protein_ratio = (food.nutrition.protein * 4) / total_macros
                    carb_ratio = (food.nutrition.carbs * 4) / total_macros
                    fat_ratio = (food.nutrition.fat * 9) / total_macros
                    
                    # Score based on how close to ideal ratios
                    score -= abs(protein_ratio - ideal_protein_ratio) * 100
                    score -= abs(carb_ratio - ideal_carb_ratio) * 100
                    score -= abs(fat_ratio - ideal_fat_ratio) * 100
            
            return score
        
        return sorted(foods, key=score_food, reverse=True)
    
    async def retrieve_relevant_foods(
        self,
        meal_type: str,
        preferences: Optional[UserPreferences] = None,
        custom_requirements: Optional[str] = None,
        n_results: int = 20
    ) -> List[FoodItem]:
        """检索相关食物."""
        
        # Build search query
        query = self._build_search_query(meal_type, preferences, custom_requirements)
        
        # Build filters
        filters = self._build_filters(meal_type, preferences)
        
        # Search in vector database
        foods = self.vector_db.search_foods(
            query=query,
            n_results=n_results * 2,  # Get more for filtering
            filters=filters
        )
        
        # Post-process filtering
        filtered_foods = self._post_filter_foods(foods, meal_type, preferences)
        
        # Rank by goal
        ranked_foods = self._rank_foods_by_goal(filtered_foods, preferences)
        
        # Return top results
        return ranked_foods[:n_results]


# Global instance
_rag_service: Optional[RAGService] = None


def get_rag_service() -> RAGService:
    """获取RAG服务单例."""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service
