"""Utility script to manage food menu data."""
import json
from pathlib import Path
from typing import List, Dict


class MenuManager:
    """菜单数据管理工具."""
    
    def __init__(self, data_file: str = "data/canteens/sample_menu.json"):
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self.menu_data = self._load_data()
    
    def _load_data(self) -> List[Dict]:
        """加载菜单数据."""
        if self.data_file.exists():
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def _save_data(self):
        """保存菜单数据."""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.menu_data, f, ensure_ascii=False, indent=2)
    
    def add_food(self, food_data: Dict):
        """添加单个食物."""
        # 检查ID是否已存在
        if any(item["id"] == food_data["id"] for item in self.menu_data):
            print(f"⚠️  Food with ID {food_data['id']} already exists!")
            return False
        
        self.menu_data.append(food_data)
        self._save_data()
        print(f"✅ Added: {food_data['name']} ({food_data['id']})")
        return True
    
    def remove_food(self, food_id: str):
        """删除食物."""
        original_count = len(self.menu_data)
        self.menu_data = [item for item in self.menu_data if item["id"] != food_id]
        
        if len(self.menu_data) < original_count:
            self._save_data()
            print(f"✅ Removed food with ID: {food_id}")
            return True
        else:
            print(f"⚠️  Food with ID {food_id} not found!")
            return False
    
    def list_foods(self, canteen: str = None):
        """列出所有食物."""
        foods = self.menu_data
        if canteen:
            foods = [f for f in foods if f["canteen"] == canteen]
        
        print(f"\n📋 Total: {len(foods)} items\n")
        print("-" * 80)
        
        for food in foods:
            print(f"ID: {food['id']}")
            print(f"名称: {food['name']}")
            print(f"食堂: {food['canteen']}")
            print(f"价格: ¥{food['price']}")
            print(f"卡路里: {food['nutrition']['calories']}kcal")
            print(f"标签: {', '.join(food['tags'])}")
            print("-" * 80)
    
    def get_canteens(self) -> List[str]:
        """获取所有食堂列表."""
        canteens = set(item["canteen"] for item in self.menu_data)
        return sorted(canteens)
    
    def stats(self):
        """显示统计信息."""
        print("\n📊 Menu Statistics\n")
        print(f"Total Items: {len(self.menu_data)}")
        
        print("\nBy Canteen:")
        for canteen in self.get_canteens():
            count = sum(1 for item in self.menu_data if item["canteen"] == canteen)
            print(f"  {canteen}: {count}")
        
        print("\nBy Category:")
        categories = {}
        for item in self.menu_data:
            cat = item["category"]
            categories[cat] = categories.get(cat, 0) + 1
        
        for cat, count in sorted(categories.items()):
            print(f"  {cat}: {count}")
        
        print("\nAverage Price:")
        avg_price = sum(item["price"] for item in self.menu_data) / len(self.menu_data)
        print(f"  ¥{avg_price:.2f}")


def interactive_add():
    """交互式添加食物."""
    manager = MenuManager()
    
    print("\n🍽️  添加新食物\n")
    
    # 显示现有食堂
    canteens = manager.get_canteens()
    print(f"现有食堂: {', '.join(canteens)}\n")
    
    # 生成ID
    existing_ids = [item["id"] for item in manager.menu_data]
    next_num = len(existing_ids) + 1
    suggested_id = f"custom_{next_num:03d}"
    
    food_data = {
        "id": input(f"ID [{suggested_id}]: ").strip() or suggested_id,
        "name": input("食物名称: ").strip(),
        "canteen": input("食堂名称: ").strip(),
        "category": input("类别 (主食/荤菜/素菜/汤/早餐/饮品): ").strip(),
        "price": float(input("价格 (元): ").strip()),
        "nutrition": {
            "calories": float(input("卡路里 (kcal): ").strip()),
            "protein": float(input("蛋白质 (g): ").strip()),
            "carbs": float(input("碳水化合物 (g): ").strip()),
            "fat": float(input("脂肪 (g): ").strip())
        },
        "ingredients": input("主要食材 (逗号分隔): ").strip().split(","),
        "tags": input("标签 (逗号分隔): ").strip().split(","),
        "available_meals": input("供应时段 (早餐/午餐/晚餐，逗号分隔): ").strip().split(","),
        "description": input("描述 (可选): ").strip() or None
    }
    
    # Clean up lists
    food_data["ingredients"] = [i.strip() for i in food_data["ingredients"] if i.strip()]
    food_data["tags"] = [t.strip() for t in food_data["tags"] if t.strip()]
    food_data["available_meals"] = [m.strip() for m in food_data["available_meals"] if m.strip()]
    
    print("\n预览:")
    print(json.dumps(food_data, ensure_ascii=False, indent=2))
    
    confirm = input("\n确认添加? (y/n): ").strip().lower()
    if confirm == 'y':
        manager.add_food(food_data)
        print("\n✅ 添加成功！记得运行 python init_db.py 更新数据库")
    else:
        print("❌ 已取消")


if __name__ == "__main__":
    import sys
    
    manager = MenuManager()
    
    if len(sys.argv) < 2:
        print("""
🍽️  菜单管理工具

用法:
  python manage_menu.py list              - 列出所有食物
  python manage_menu.py list <canteen>    - 列出指定食堂的食物
  python manage_menu.py stats             - 显示统计信息
  python manage_menu.py add               - 交互式添加食物
  python manage_menu.py remove <id>       - 删除指定ID的食物

示例:
  python manage_menu.py list 中心食堂
  python manage_menu.py remove c1_001
        """)
    else:
        command = sys.argv[1]
        
        if command == "list":
            canteen = sys.argv[2] if len(sys.argv) > 2 else None
            manager.list_foods(canteen)
        
        elif command == "stats":
            manager.stats()
        
        elif command == "add":
            interactive_add()
        
        elif command == "remove":
            if len(sys.argv) < 3:
                print("❌ 请提供要删除的食物ID")
            else:
                manager.remove_food(sys.argv[2])
        
        else:
            print(f"❌ 未知命令: {command}")
