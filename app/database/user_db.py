"""User database using SQLite."""
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from datetime import datetime
from typing import Optional, List
import json
from app.config import get_settings
from app.models import User, UserPreferences, FoodHistory

Base = declarative_base()


class UserModel(Base):
    """用户表模型."""
    __tablename__ = "users"
    
    user_id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=False)
    preferences = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    last_active = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class FoodHistoryModel(Base):
    """饮食历史表模型."""
    __tablename__ = "food_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, index=True, nullable=False)
    food_id = Column(String, nullable=False)
    food_name = Column(String, nullable=False)
    canteen = Column(String, nullable=False)
    meal_type = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    rating = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)


class UserDatabase:
    """用户数据库管理类."""
    
    def __init__(self):
        """Initialize database."""
        self.settings = get_settings()
        self.engine = create_async_engine(
            self.settings.database_url,
            echo=self.settings.debug
        )
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
    
    async def init_db(self):
        """初始化数据库表."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def create_user(self, user: User) -> User:
        """创建新用户."""
        async with self.async_session() as session:
            user_model = UserModel(
                user_id=user.user_id,
                username=user.username,
                preferences=user.preferences.model_dump() if user.preferences else None,
                created_at=user.created_at,
                last_active=user.last_active
            )
            session.add(user_model)
            await session.commit()
            return user
    
    async def get_user(self, user_id: str) -> Optional[User]:
        """获取用户信息."""
        async with self.async_session() as session:
            result = await session.get(UserModel, user_id)
            if result:
                return User(
                    user_id=result.user_id,
                    username=result.username,
                    preferences=UserPreferences(**result.preferences) if result.preferences else None,
                    created_at=result.created_at,
                    last_active=result.last_active
                )
            return None
    
    async def update_user_preferences(
        self, user_id: str, preferences: UserPreferences
    ) -> Optional[User]:
        """更新用户偏好."""
        async with self.async_session() as session:
            user = await session.get(UserModel, user_id)
            if user:
                user.preferences = preferences.model_dump()
                user.last_active = datetime.now()
                await session.commit()
                return await self.get_user(user_id)
            return None
    
    async def add_food_history(self, history: FoodHistory) -> FoodHistory:
        """添加饮食历史记录."""
        async with self.async_session() as session:
            history_model = FoodHistoryModel(
                user_id=history.user_id,
                food_id=history.food_id,
                food_name=history.food_name,
                canteen=history.canteen,
                meal_type=history.meal_type,
                timestamp=history.timestamp,
                rating=history.rating,
                notes=history.notes
            )
            session.add(history_model)
            await session.commit()
            return history
    
    async def get_user_history(
        self, user_id: str, limit: int = 50
    ) -> List[FoodHistory]:
        """获取用户饮食历史."""
        async with self.async_session() as session:
            from sqlalchemy import select
            stmt = select(FoodHistoryModel).where(
                FoodHistoryModel.user_id == user_id
            ).order_by(FoodHistoryModel.timestamp.desc()).limit(limit)
            result = await session.execute(stmt)
            histories = result.scalars().all()
            
            return [
                FoodHistory(
                    user_id=h.user_id,
                    food_id=h.food_id,
                    food_name=h.food_name,
                    canteen=h.canteen,
                    meal_type=h.meal_type,
                    timestamp=h.timestamp,
                    rating=h.rating,
                    notes=h.notes
                ) for h in histories
            ]


# Global instance
_user_db: Optional[UserDatabase] = None


async def get_user_db() -> UserDatabase:
    """获取用户数据库单例."""
    global _user_db
    if _user_db is None:
        _user_db = UserDatabase()
        await _user_db.init_db()
    return _user_db
