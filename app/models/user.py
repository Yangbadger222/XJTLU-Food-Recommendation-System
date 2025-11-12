"""Data models for users."""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class FitnessGoal(str, Enum):
    """健身目标枚举."""
    LOSE_WEIGHT = "减脂"
    GAIN_MUSCLE = "增肌"
    MAINTAIN = "保持"
    BALANCED = "均衡饮食"


class UserPreferences(BaseModel):
    """用户偏好设置."""
    goal: FitnessGoal = Field(..., description="健身目标")
    daily_calories_target: Optional[int] = Field(None, description="每日目标卡路里")
    dietary_restrictions: List[str] = Field(default_factory=list, description="饮食限制 (无辣/素食/清真等)")
    allergies: List[str] = Field(default_factory=list, description="过敏食材")
    preferred_canteens: List[str] = Field(default_factory=list, description="偏好的食堂")
    disliked_foods: List[str] = Field(default_factory=list, description="不喜欢的食物")


class FoodHistory(BaseModel):
    """饮食历史记录."""
    user_id: str
    food_id: str
    food_name: str
    canteen: str
    meal_type: str  # 早餐/午餐/晚餐
    timestamp: datetime = Field(default_factory=datetime.now)
    rating: Optional[int] = Field(None, ge=1, le=5, description="评分 1-5")
    notes: Optional[str] = Field(None, description="备注")


class User(BaseModel):
    """用户模型."""
    user_id: str = Field(..., description="用户唯一标识")
    username: str = Field(..., description="用户名")
    preferences: Optional[UserPreferences] = Field(None, description="用户偏好")
    created_at: datetime = Field(default_factory=datetime.now)
    last_active: datetime = Field(default_factory=datetime.now)


class RecommendationRequest(BaseModel):
    """推荐请求模型."""
    user_id: str = Field(..., description="用户ID")
    meal_type: str = Field(..., description="餐次 (早餐/午餐/晚餐)")
    preferences: Optional[UserPreferences] = Field(None, description="临时偏好设置")
    custom_requirements: Optional[str] = Field(None, description="自定义要求")
