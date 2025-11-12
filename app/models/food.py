"""Data models for food items."""
from typing import Optional, List
from pydantic import BaseModel, Field


class NutritionInfo(BaseModel):
    """营养信息模型."""
    calories: float = Field(..., description="卡路里 (kcal)")
    protein: float = Field(..., description="蛋白质 (g)")
    carbs: float = Field(..., description="碳水化合物 (g)")
    fat: float = Field(..., description="脂肪 (g)")
    fiber: Optional[float] = Field(None, description="纤维 (g)")
    sodium: Optional[float] = Field(None, description="钠 (mg)")


class FoodItem(BaseModel):
    """食物条目模型."""
    id: str = Field(..., description="食物唯一标识")
    name: str = Field(..., description="食物名称")
    canteen: str = Field(..., description="食堂名称")
    category: str = Field(..., description="类别 (主食/荤菜/素菜/汤/饮品)")
    price: float = Field(..., description="价格 (元)")
    nutrition: NutritionInfo = Field(..., description="营养信息")
    ingredients: List[str] = Field(default_factory=list, description="主要食材")
    tags: List[str] = Field(default_factory=list, description="标签 (辣/清淡/健康等)")
    available_meals: List[str] = Field(default_factory=list, description="供应时段 (早餐/午餐/晚餐)")
    description: Optional[str] = Field(None, description="描述")
    

class FoodRecommendation(BaseModel):
    """食物推荐结果."""
    food_items: List[FoodItem] = Field(..., description="推荐的食物")
    total_nutrition: NutritionInfo = Field(..., description="总营养信息")
    reasoning: str = Field(..., description="推荐理由")
    tips: Optional[str] = Field(None, description="饮食建议")
