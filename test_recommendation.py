"""Example script to test the recommendation system."""
import asyncio
import json
from app.models import User, UserPreferences, FitnessGoal, RecommendationRequest
from app.services import get_recommendation_service
from app.database import get_user_db


async def test_recommendation():
    """Test the recommendation system with sample data."""
    print("🧪 Testing XJTLU Food Recommendation System\n")
    
    # 1. Create a test user
    print("1️⃣ Creating test user...")
    user = User(
        user_id="test_user_001",
        username="张三",
        preferences=UserPreferences(
            goal=FitnessGoal.LOSE_WEIGHT,
            daily_calories_target=1500,
            dietary_restrictions=["清淡"],
            allergies=["花生"],
            preferred_canteens=["中心食堂", "北区食堂"],
            disliked_foods=["麻辣香锅"]
        )
    )
    
    user_db = await get_user_db()
    
    # Check if user exists, if so, just use it
    existing_user = await user_db.get_user(user.user_id)
    if not existing_user:
        await user_db.create_user(user)
        print(f"✅ Created user: {user.username}\n")
    else:
        print(f"✅ Using existing user: {existing_user.username}\n")
    
    # 2. Test recommendation
    print("2️⃣ Getting lunch recommendation for weight loss...")
    request = RecommendationRequest(
        user_id=user.user_id,
        meal_type="午餐",
        custom_requirements="我想要高蛋白低脂肪的食物"
    )
    
    service = get_recommendation_service()
    recommendation = await service.get_recommendation(request)
    
    print("\n📋 Recommendation Results:\n")
    print("=" * 60)
    
    print("\n🍽️ Recommended Foods:")
    for i, food in enumerate(recommendation.food_items, 1):
        print(f"\n{i}. {food.name} - {food.canteen}")
        print(f"   💰 Price: ¥{food.price}")
        print(f"   🔥 Calories: {food.nutrition.calories} kcal")
        print(f"   💪 Protein: {food.nutrition.protein}g")
        print(f"   🍚 Carbs: {food.nutrition.carbs}g")
        print(f"   🥑 Fat: {food.nutrition.fat}g")
        print(f"   🏷️ Tags: {', '.join(food.tags)}")
    
    print("\n" + "=" * 60)
    print("\n📊 Total Nutrition:")
    print(f"   Total Calories: {recommendation.total_nutrition.calories} kcal")
    print(f"   Total Protein: {recommendation.total_nutrition.protein}g")
    print(f"   Total Carbs: {recommendation.total_nutrition.carbs}g")
    print(f"   Total Fat: {recommendation.total_nutrition.fat}g")
    
    print("\n" + "=" * 60)
    print("\n💡 Reasoning:")
    print(recommendation.reasoning)
    
    if recommendation.tips:
        print("\n" + "=" * 60)
        print("\n🎯 Tips:")
        print(recommendation.tips)
    
    print("\n" + "=" * 60)
    
    # 3. Test another scenario
    print("\n\n3️⃣ Getting breakfast recommendation for muscle gain...")
    
    # Update user preferences
    new_preferences = UserPreferences(
        goal=FitnessGoal.GAIN_MUSCLE,
        daily_calories_target=2500,
        dietary_restrictions=[],
        allergies=["花生"],
        preferred_canteens=[],
        disliked_foods=[]
    )
    
    await user_db.update_user_preferences(user.user_id, new_preferences)
    
    request2 = RecommendationRequest(
        user_id=user.user_id,
        meal_type="早餐"
    )
    
    recommendation2 = await service.get_recommendation(request2)
    
    print("\n🍽️ Breakfast Recommendations:")
    for i, food in enumerate(recommendation2.food_items, 1):
        print(f"{i}. {food.name} ({food.nutrition.calories}kcal, {food.nutrition.protein}g蛋白质)")
    
    print("\n✅ Test completed successfully!")


if __name__ == "__main__":
    asyncio.run(test_recommendation())
