"""快速批量导入食物数据."""
import json
from pathlib import Path
from manage_menu import MenuManager


def import_from_json(json_file: str):
    """从JSON文件批量导入食物."""
    manager = MenuManager()
    
    json_path = Path(json_file)
    if not json_path.exists():
        print(f"❌ 文件不存在: {json_file}")
        return
    
    print(f"📖 正在读取: {json_file}")
    
    with open(json_path, "r", encoding="utf-8") as f:
        new_foods = json.load(f)
    
    if not isinstance(new_foods, list):
        new_foods = [new_foods]
    
    success_count = 0
    fail_count = 0
    
    for food in new_foods:
        if manager.add_food(food):
            success_count += 1
        else:
            fail_count += 1
    
    print(f"\n✅ 成功导入: {success_count} 个")
    if fail_count > 0:
        print(f"❌ 失败: {fail_count} 个")
    
    print(f"\n📊 当前总数: {len(manager.menu_data)} 个食物")
    print("\n⚠️  别忘了运行 'python init_db.py' 更新数据库！")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("""
📥 批量导入食物数据

用法:
  python import_foods.py <json文件路径>

示例:
  python import_foods.py data/canteens/new_foods.json
  python import_foods.py my_foods.json

JSON 格式示例:
[
  {
    "id": "custom_001",
    "name": "食物名称",
    "canteen": "食堂名称",
    "category": "类别",
    "price": 15.0,
    "nutrition": {
      "calories": 300,
      "protein": 20,
      "carbs": 40,
      "fat": 8
    },
    "ingredients": ["食材1", "食材2"],
    "tags": ["标签1", "标签2"],
    "available_meals": ["午餐", "晚餐"],
    "description": "描述"
  }
]
        """)
    else:
        import_from_json(sys.argv[1])
