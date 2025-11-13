# 🚀 快速开始：添加RAG食物数据

## ✅ 已完成！

您的系统现在有 **20个食物**，包括：
- 希腊酸奶碗（早餐）
- 豆浆油条（传统早餐）
- 蛋白奶昔（运动补充）
- 全麦贝果（健康早餐）
- 运动能量棒（便携小食）

---

## 📖 三种添加方法

### 方法一：交互式添加（最简单）

```powershell
# 双击运行这个脚本
add_food_interactive.bat

# 或在终端运行
python manage_menu.py add
```

按提示填写信息即可！

---

### 方法二：批量导入JSON（最高效）

**步骤1**: 创建 JSON 文件（如 `my_foods.json`）

```json
[
  {
    "id": "custom_001",
    "name": "牛排套餐",
    "canteen": "中心食堂",
    "category": "主食",
    "price": 35.0,
    "nutrition": {
      "calories": 680,
      "protein": 55,
      "carbs": 48,
      "fat": 25
    },
    "ingredients": ["牛排", "土豆", "西兰花"],
    "tags": ["高蛋白", "增肌", "高热量"],
    "available_meals": ["午餐", "晚餐"],
    "description": "优质牛排配蔬菜"
  }
]
```

**步骤2**: 导入并更新

```powershell
python import_foods.py my_foods.json
python init_db.py
```

---

### 方法三：编辑JSON文件（最直接）

**步骤1**: 打开文件

```
data/canteens/sample_menu.json
```

**步骤2**: 在数组末尾添加新对象

```json
{
  "id": "c1_999",
  "name": "新食物",
  ...
}
```

**步骤3**: 更新数据库

```powershell
python init_db.py
```

---

## 🔧 常用命令速查

```powershell
# 查看统计
check_database.bat
# 或
python test_search.py stats

# 搜索测试
search_food.bat "减脂 高蛋白"
# 或
python test_search.py "关键词" 5

# 查看所有食物
python manage_menu.py list

# 查看特定食堂
python manage_menu.py list 中心食堂

# 删除食物
python manage_menu.py remove food_id
```

---

## 📋 字段模板

复制这个模板快速创建新食物：

```json
{
  "id": "c1_XXX",
  "name": "食物名称",
  "canteen": "中心食堂/南门食堂/北门食堂/体育馆餐厅",
  "category": "主食/荤菜/素菜/汤/早餐/饮品",
  "price": 0.0,
  "nutrition": {
    "calories": 0,
    "protein": 0,
    "carbs": 0,
    "fat": 0
  },
  "ingredients": ["食材1", "食材2"],
  "tags": ["标签1", "标签2"],
  "available_meals": ["早餐/午餐/晚餐"],
  "description": "可选描述"
}
```

---

## 🏷️ 推荐标签

**健康目标**：`减脂` `增肌` `健康` `清淡`

**营养特点**：`高蛋白` `低脂` `低卡` `高纤维`

**食材类型**：`素食` `海鲜` `肉类` `辣`

**使用场景**：`快手` `经济实惠` `特色` `运动` `便携`

---

## 💡 营养数据参考

### 常见食物营养（每份）

| 食物 | 卡路里 | 蛋白质 | 碳水 | 脂肪 |
|-----|--------|--------|------|------|
| 鸡胸肉(100g) | 165 | 31g | 0g | 3.6g |
| 鸡蛋(1个) | 155 | 13g | 1g | 11g |
| 米饭(1碗) | 206 | 4g | 45g | 0.4g |
| 西兰花(100g) | 34 | 2.8g | 7g | 0.4g |
| 牛油果(1个) | 234 | 3g | 12g | 21g |
| 三文鱼(100g) | 206 | 22g | 0g | 13g |

### 餐次建议

| 餐次 | 卡路里 | 蛋白质 | 碳水 | 脂肪 |
|-----|--------|--------|------|------|
| 早餐 | 400-500 | 15-20g | 50-60g | 10-15g |
| 午餐 | 600-800 | 25-35g | 70-90g | 15-25g |
| 晚餐 | 500-700 | 20-30g | 60-80g | 12-20g |

---

## ⚠️ 注意事项

1. ✅ **ID必须唯一** - 使用 `python manage_menu.py list` 检查现有ID
2. ✅ **标签统一** - 使用 `减脂` 而非 `减肥`，保持术语一致
3. ✅ **更新数据库** - 每次修改后必须运行 `python init_db.py`
4. ✅ **营养准确性** - 参考权威数据源
5. ✅ **备份数据** - 修改前备份 `sample_menu.json`

---

## 🔍 验证添加结果

添加食物后，运行测试确保正确：

```powershell
# 查看总数
python test_search.py stats

# 搜索新食物
python test_search.py "新食物的关键词"

# 在浏览器测试
# 访问 http://127.0.0.1:8000
# 尝试获取推荐，看是否出现新食物
```

---

## 🎯 实战示例

### 示例1: 添加一个减脂餐

```json
{
  "id": "c1_100",
  "name": "健康鸡胸肉沙拉",
  "canteen": "中心食堂",
  "category": "主食",
  "price": 18.0,
  "nutrition": {
    "calories": 320,
    "protein": 42,
    "carbs": 25,
    "fat": 6
  },
  "ingredients": ["鸡胸肉", "生菜", "圣女果", "黄瓜", "橄榄油"],
  "tags": ["减脂", "高蛋白", "低脂", "低卡", "健康"],
  "available_meals": ["午餐", "晚餐"],
  "description": "低卡高蛋白，减脂期首选"
}
```

### 示例2: 添加一个增肌餐

```json
{
  "id": "c1_101",
  "name": "牛肉饭套餐",
  "canteen": "中心食堂",
  "category": "主食",
  "price": 25.0,
  "nutrition": {
    "calories": 720,
    "protein": 48,
    "carbs": 82,
    "fat": 18
  },
  "ingredients": ["牛肉", "米饭", "鸡蛋", "西兰花"],
  "tags": ["增肌", "高蛋白", "高热量", "健康"],
  "available_meals": ["午餐", "晚餐"],
  "description": "高蛋白高热量，增肌必备"
}
```

### 示例3: 添加一个快手早餐

```json
{
  "id": "c1_102",
  "name": "全麦三明治套餐",
  "canteen": "中心食堂",
  "category": "早餐",
  "price": 12.0,
  "nutrition": {
    "calories": 380,
    "protein": 18,
    "carbs": 45,
    "fat": 12
  },
  "ingredients": ["全麦面包", "火腿", "生菜", "番茄", "鸡蛋"],
  "tags": ["早餐", "快手", "健康", "便携"],
  "available_meals": ["早餐"],
  "description": "营养均衡的快手早餐"
}
```

---

## 🚀 批量添加示例

创建 `my_new_foods.json`：

```json
[
  { "id": "c1_100", "name": "健康鸡胸肉沙拉", ... },
  { "id": "c1_101", "name": "牛肉饭套餐", ... },
  { "id": "c1_102", "name": "全麦三明治套餐", ... }
]
```

一键导入：

```powershell
python import_foods.py my_new_foods.json
python init_db.py
```

---

## 🌐 Web界面查看

打开浏览器访问：

```
http://127.0.0.1:8000/how_to_add_foods.html
```

这是一个交互式的添加指南网页！

---

## 📚 更多资源

- 📖 **完整文档**: `ADD_FOOD_GUIDE.md`
- 🌐 **Web指南**: `http://localhost:8000/how_to_add_foods.html`
- 📊 **数据文件**: `data/canteens/sample_menu.json`
- 🔧 **管理工具**: `manage_menu.py`

---

## ✨ 提示

1. 食物越多，AI推荐越准确
2. 标签要精准，帮助AI理解
3. 营养数据要真实，不要瞎编
4. 定期备份 JSON 文件
5. 使用 `--reload` 运行服务器，自动重载数据

---

**现在您可以：**

✅ 双击 `add_food_interactive.bat` 交互式添加  
✅ 双击 `check_database.bat` 查看统计  
✅ 创建 JSON 文件批量导入  
✅ 直接编辑 `sample_menu.json`  

**记得每次修改后运行 `python init_db.py`！** 🎉
