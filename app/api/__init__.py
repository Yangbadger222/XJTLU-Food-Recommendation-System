"""API package."""
from .recommend import router as recommend_router
from .user import router as user_router
from .chat import router as chat_router

__all__ = ["recommend_router", "user_router", "chat_router"]
