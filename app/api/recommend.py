"""Recommendation API routes."""
from fastapi import APIRouter, HTTPException
from app.models import RecommendationRequest, FoodRecommendation
from app.services import get_recommendation_service

router = APIRouter(prefix="/api/recommend", tags=["recommendations"])


@router.post("", response_model=FoodRecommendation)
async def get_recommendation(request: RecommendationRequest):
    """
    获取食物推荐.
    
    根据用户的偏好设置、健康目标和餐次，返回个性化的食物推荐。
    """
    try:
        service = get_recommendation_service()
        recommendation = await service.get_recommendation(request)
        return recommendation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"推荐生成失败: {str(e)}")


@router.get("/health")
async def health_check():
    """健康检查端点."""
    return {"status": "healthy", "service": "recommendation"}
