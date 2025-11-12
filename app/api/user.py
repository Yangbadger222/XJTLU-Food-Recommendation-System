"""User management API routes."""
from fastapi import APIRouter, HTTPException
from typing import List
from app.models import User, UserPreferences, FoodHistory
from app.database import get_user_db

router = APIRouter(prefix="/api/user", tags=["users"])


@router.post("", response_model=User)
async def create_user(user: User):
    """
    创建新用户.
    """
    try:
        user_db = await get_user_db()
        
        # Check if user exists
        existing = await user_db.get_user(user.user_id)
        if existing:
            raise HTTPException(status_code=400, detail="用户已存在")
        
        created_user = await user_db.create_user(user)
        return created_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建用户失败: {str(e)}")


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    """
    获取用户信息.
    """
    try:
        user_db = await get_user_db()
        user = await user_db.get_user(user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户失败: {str(e)}")


@router.put("/{user_id}/preferences", response_model=User)
async def update_preferences(user_id: str, preferences: UserPreferences):
    """
    更新用户偏好设置.
    """
    try:
        user_db = await get_user_db()
        user = await user_db.update_user_preferences(user_id, preferences)
        
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新偏好失败: {str(e)}")


@router.post("/history", response_model=FoodHistory)
async def add_food_history(history: FoodHistory):
    """
    添加饮食历史记录.
    """
    try:
        user_db = await get_user_db()
        created_history = await user_db.add_food_history(history)
        return created_history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"添加历史记录失败: {str(e)}")


@router.get("/{user_id}/history", response_model=List[FoodHistory])
async def get_user_history(user_id: str, limit: int = 50):
    """
    获取用户饮食历史.
    """
    try:
        user_db = await get_user_db()
        history = await user_db.get_user_history(user_id, limit)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取历史记录失败: {str(e)}")
