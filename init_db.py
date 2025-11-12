"""Script to initialize the database with sample data."""
import asyncio
import json
from pathlib import Path
from app.models import FoodItem
from app.database import get_vector_db


async def init_database():
    """Initialize the vector database with sample food data."""
    print("🍜 Initializing XJTLU Food Recommendation System Database...")
    
    # Load sample menu data
    data_path = Path("data/canteens/sample_menu.json")
    
    if not data_path.exists():
        print(f"❌ Error: {data_path} not found!")
        return
    
    with open(data_path, "r", encoding="utf-8") as f:
        menu_data = json.load(f)
    
    # Convert to FoodItem objects
    food_items = [FoodItem(**item) for item in menu_data]
    
    print(f"📦 Loaded {len(food_items)} food items from sample menu")
    
    # Initialize vector database
    vector_db = get_vector_db()
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    current_count = vector_db.count()
    if current_count > 0:
        print(f"⚠️  Found {current_count} existing items. Clearing database...")
        vector_db.clear_all()
    
    # Add food items to database
    print("📝 Adding food items to vector database...")
    vector_db.add_food_items(food_items)
    
    print(f"✅ Successfully added {len(food_items)} items to database")
    print(f"📊 Total items in database: {vector_db.count()}")
    
    # Test search
    print("\n🔍 Testing search functionality...")
    test_results = vector_db.search_foods("减脂 高蛋白 午餐", n_results=3)
    
    print(f"\nFound {len(test_results)} results for '减脂 高蛋白 午餐':")
    for i, food in enumerate(test_results, 1):
        print(f"{i}. {food.name} - {food.canteen} ({food.nutrition.calories}kcal, {food.nutrition.protein}g蛋白质)")
    
    print("\n✨ Database initialization complete!")


if __name__ == "__main__":
    asyncio.run(init_database())
