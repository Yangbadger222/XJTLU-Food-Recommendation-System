"""DeepSeek API service with context management."""
from openai import AsyncOpenAI
from typing import List, Dict, Optional
from app.config import get_settings
from app.models import FoodItem, UserPreferences, FitnessGoal


class DeepSeekService:
    """DeepSeek API服务类，用于与AI模型交互."""
    
    def __init__(self):
        """Initialize DeepSeek API client."""
        self.settings = get_settings()
        self.client = AsyncOpenAI(
            api_key=self.settings.deepseek_api_key,
            base_url=self.settings.deepseek_api_base
        )
        self.model = self.settings.deepseek_model
        self.temperature = self.settings.temperature
    
    def _build_system_prompt(self) -> str:
        """构建系统提示词."""
        return """你是西交利物浦大学的AI营养顾问助手。你的任务是根据学生的健康目标和饮食偏好，
从学校周围食堂的真实菜单中推荐合适的食物。

你需要：
1. 理解用户的健康目标（减脂、增肌、均衡饮食等）
2. 考虑用户的饮食限制和过敏信息
3. 基于提供的食堂菜单数据进行推荐
4. 给出清晰的营养分析和推荐理由
5. 提供实用的饮食建议

重要原则：
- 所有推荐必须基于提供的菜单数据，不要推荐不存在的食物
- 注重营养均衡和健康
- 考虑学生的预算
- 给出具体的理由和建议
"""
    
    def _build_user_context(
        self,
        preferences: Optional[UserPreferences],
        meal_type: str,
        recent_history: Optional[List[str]] = None
    ) -> str:
        """构建用户上下文信息."""
        context = f"餐次: {meal_type}\n\n"
        
        if preferences:
            context += f"健康目标: {preferences.goal.value}\n"
            
            if preferences.daily_calories_target:
                context += f"每日目标卡路里: {preferences.daily_calories_target}kcal\n"
            
            if preferences.dietary_restrictions:
                context += f"饮食限制: {', '.join(preferences.dietary_restrictions)}\n"
            
            if preferences.allergies:
                context += f"过敏食材: {', '.join(preferences.allergies)}\n"
            
            if preferences.preferred_canteens:
                context += f"偏好食堂: {', '.join(preferences.preferred_canteens)}\n"
            
            if preferences.disliked_foods:
                context += f"不喜欢的食物: {', '.join(preferences.disliked_foods)}\n"
        
        if recent_history:
            context += f"\n最近饮食历史（用于了解饮食习惯）:\n"
            for item in recent_history[:10]:  # 最近10条
                context += f"- {item}\n"
        
        return context
    
    def _format_food_items(self, foods: List[FoodItem]) -> str:
        """格式化食物列表为文本."""
        formatted = "可选择的食物:\n\n"
        for food in foods:
            formatted += f"""
【{food.name}】
- 食堂: {food.canteen}
- 类别: {food.category}
- 价格: {food.price}元
- 营养: 卡路里{food.nutrition.calories}kcal, 蛋白质{food.nutrition.protein}g, 碳水{food.nutrition.carbs}g, 脂肪{food.nutrition.fat}g
- 食材: {', '.join(food.ingredients)}
- 标签: {', '.join(food.tags)}
---
"""
        return formatted
    
    async def generate_recommendation(
        self,
        available_foods: List[FoodItem],
        preferences: Optional[UserPreferences] = None,
        meal_type: str = "午餐",
        recent_history: Optional[List[str]] = None,
        custom_requirements: Optional[str] = None
    ) -> str:
        """生成食物推荐."""
        
        # Build messages
        messages = [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user", "content": self._build_user_context(preferences, meal_type, recent_history)},
            {"role": "user", "content": self._format_food_items(available_foods)}
        ]
        
        # Add custom requirements if provided
        if custom_requirements:
            messages.append({
                "role": "user",
                "content": f"额外要求: {custom_requirements}"
            })
        
        # Add final instruction
        messages.append({
            "role": "user",
            "content": """请从上述食物中推荐2-4道菜，组成一顿营养均衡的餐食。

请按以下格式回复：

**推荐菜品：**
1. [菜名1] - [食堂名]
2. [菜名2] - [食堂名]
...

**营养分析：**
- 总卡路里: XXX kcal
- 总蛋白质: XX g
- 总碳水: XX g
- 总脂肪: XX g

**推荐理由：**
[解释为什么推荐这些菜品，如何符合用户的健康目标]

**饮食建议：**
[给出一些实用的饮食建议]
"""
        })
        
        # Call API
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    async def chat(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """通用聊天接口，用于回答用户问题."""
        messages = [
            {"role": "system", "content": self._build_system_prompt()}
        ]
        
        if conversation_history:
            messages.extend(conversation_history)
        
        messages.append({"role": "user", "content": user_message})
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=500
        )
        
        return response.choices[0].message.content


# Global instance
_deepseek_service: Optional[DeepSeekService] = None


def get_deepseek_service() -> DeepSeekService:
    """获取DeepSeek服务单例."""
    global _deepseek_service
    if _deepseek_service is None:
        _deepseek_service = DeepSeekService()
    return _deepseek_service
