"""Vector database for RAG system using ChromaDB."""
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
from app.config import get_settings
from app.models import FoodItem


class VectorDatabase:
    """向量数据库管理类，用于存储和检索食物数据."""
    
    def __init__(self):
        """Initialize vector database."""
        self.settings = get_settings()
        self.db_path = Path(self.settings.vector_db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(self.db_path),
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(self.settings.embedding_model)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="food_items",
            metadata={"description": "XJTLU canteen food items"}
        )
    
    def _create_food_document(self, food: FoodItem) -> str:
        """创建食物的文本表示用于嵌入."""
        doc = f"""
        食物名称: {food.name}
        食堂: {food.canteen}
        类别: {food.category}
        价格: {food.price}元
        营养信息: 
        - 卡路里: {food.nutrition.calories}kcal
        - 蛋白质: {food.nutrition.protein}g
        - 碳水: {food.nutrition.carbs}g
        - 脂肪: {food.nutrition.fat}g
        食材: {', '.join(food.ingredients)}
        标签: {', '.join(food.tags)}
        供应时段: {', '.join(food.available_meals)}
        """
        if food.description:
            doc += f"\n描述: {food.description}"
        return doc.strip()
    
    def add_food_items(self, foods: List[FoodItem]) -> None:
        """添加食物条目到向量数据库."""
        if not foods:
            return
        
        documents = [self._create_food_document(food) for food in foods]
        metadatas = [food.model_dump() for food in foods]
        ids = [food.id for food in foods]
        
        # Convert metadata to JSON strings for nested objects
        for metadata in metadatas:
            metadata['nutrition'] = json.dumps(metadata['nutrition'])
            metadata['ingredients'] = json.dumps(metadata['ingredients'])
            metadata['tags'] = json.dumps(metadata['tags'])
            metadata['available_meals'] = json.dumps(metadata['available_meals'])
        
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def search_foods(
        self,
        query: str,
        n_results: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[FoodItem]:
        """根据查询搜索相关食物."""
        where = filters if filters else None
        
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where
        )
        
        if not results['metadatas'] or not results['metadatas'][0]:
            return []
        
        foods = []
        for metadata in results['metadatas'][0]:
            # Parse JSON strings back to objects
            metadata['nutrition'] = json.loads(metadata['nutrition'])
            metadata['ingredients'] = json.loads(metadata['ingredients'])
            metadata['tags'] = json.loads(metadata['tags'])
            metadata['available_meals'] = json.loads(metadata['available_meals'])
            foods.append(FoodItem(**metadata))
        
        return foods
    
    def get_food_by_id(self, food_id: str) -> Optional[FoodItem]:
        """根据ID获取食物."""
        try:
            result = self.collection.get(ids=[food_id])
            if result['metadatas']:
                metadata = result['metadatas'][0]
                metadata['nutrition'] = json.loads(metadata['nutrition'])
                metadata['ingredients'] = json.loads(metadata['ingredients'])
                metadata['tags'] = json.loads(metadata['tags'])
                metadata['available_meals'] = json.loads(metadata['available_meals'])
                return FoodItem(**metadata)
        except Exception:
            return None
        return None
    
    def clear_all(self) -> None:
        """清空数据库 (谨慎使用)."""
        self.client.delete_collection("food_items")
        self.collection = self.client.get_or_create_collection(
            name="food_items",
            metadata={"description": "XJTLU canteen food items"}
        )
    
    def count(self) -> int:
        """返回数据库中的食物数量."""
        return self.collection.count()


# Global instance
_vector_db: Optional[VectorDatabase] = None


def get_vector_db() -> VectorDatabase:
    """获取向量数据库单例."""
    global _vector_db
    if _vector_db is None:
        _vector_db = VectorDatabase()
    return _vector_db
