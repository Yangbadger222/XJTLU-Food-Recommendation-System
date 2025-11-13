# 🍜 XJTLU 智能食堂推荐系统# 🍜 西浦智能食物推荐系统



<div align="center">基于DeepSeek API和RAG技术的AI智能食物推荐系统，帮助西浦学生根据个人需求（健身、减脂等）获得个性化饮食推荐。



[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)> 

[![FastAPI](https://img.shields.io/badge/FastAPI-0.121.1-009688.svg)](https://fastapi.tiangolo.com)

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)## ✨ 核心特性

[![DeepSeek](https://img.shields.io/badge/AI-DeepSeek-purple.svg)](https://deepseek.com)

- 🤖 **智能推荐**: 基于DeepSeek API的上下文理解能力

**基于 RAG 和 AI 的智能营养推荐系统**- 📚 **RAG技术**: 使用检索增强生成，确保推荐基于真实菜单数据

- 🎯 **个性化**: 学习用户饮食习惯，提供定制化建议

为西交利物浦大学学生提供个性化的食堂饮食建议- 💪 **健康目标**: 支持减脂、增肌、均衡饮食等多种目标

- 🏫 **本地化**: 专注西浦周围食堂的真实菜单

[功能特点](#-功能特点) • [技术栈](#-技术栈) • [快速开始](#-快速开始) • [使用指南](#-使用指南) • [部署](#-部署)

## 🏗️ 技术栈

</div>

### 后端

---- **Python 3.10+**

- **FastAPI**: 高性能Web框架

## 📖 项目简介- **DeepSeek API**: 大语言模型

- **ChromaDB**: 向量数据库

XJTLU 智能食堂推荐系统是一个基于人工智能的饮食推荐平台，旨在帮助西交利物浦大学的学生：- **SQLite**: 用户数据存储



- 🎯 **个性化推荐**：根据健康目标（减脂、增肌、均衡饮食）智能推荐食物### 部署

- 🥗 **营养分析**：详细的卡路里、蛋白质、碳水化合物、脂肪含量分析- **GitHub Actions**: CI/CD

- 🤖 **AI 营养师**：24/7 在线 AI 助手，解答饮食营养问题- **免费部署选项**: Render/Railway/Vercel

- 📊 **饮食追踪**：记录和分析个人饮食历史

- 🔒 **隐私保护**：基于 RAG 技术，确保 AI 推荐符合伦理标准## 📦 项目结构



---```

recommend/

## ✨ 功能特点├── app/

│   ├── __init__.py

### 🎨 用户界面│   ├── main.py                 # FastAPI应用入口

- 现代化渐变紫色主题设计│   ├── config.py               # 配置管理

- 响应式布局，支持移动端│   ├── models/                 # 数据模型

- 实时 AI 聊天对话│   │   ├── __init__.py

- 直观的食物推荐展示│   │   ├── user.py

│   │   └── food.py

### 🧠 AI 功能│   ├── services/               # 业务逻辑

- **RAG（检索增强生成）**：结合向量数据库和大语言模型│   │   ├── __init__.py

- **上下文学习**：AI 会记住用户的饮食习惯│   │   ├── deepseek_service.py # DeepSeek API集成

- **智能对话**：自然语言交互，理解复杂需求│   │   ├── rag_service.py      # RAG检索服务

- **实时推荐**：基于用户偏好和健康目标的即时建议│   │   └── recommendation.py   # 推荐逻辑

│   ├── database/               # 数据库

### 📊 数据管理│   │   ├── __init__.py

- SQLite 用户数据存储│   │   ├── vector_db.py        # 向量数据库

- ChromaDB 向量数据库用于食物检索│   │   └── user_db.py          # 用户数据库

- 用户偏好和历史记录追踪│   └── api/                    # API路由

- 支持批量导入食堂菜单数据│       ├── __init__.py

│       ├── recommend.py

---│       └── user.py

├── data/

## 🛠️ 技术栈│   ├── canteens/               # 食堂菜单数据

│   │   ├── canteen1.json

### 后端框架│   │   └── canteen2.json

- **FastAPI** `0.121.1` - 高性能异步 Web 框架│   └── nutrition/              # 营养数据

- **Uvicorn** `0.38.0` - ASGI 服务器├── tests/                      # 测试文件

- **Python** `3.12+` - 主要开发语言├── .env.example                # 环境变量示例

├── .gitignore

### AI & 机器学习├── requirements.txt

- **DeepSeek API** - 大语言模型（OpenAI 兼容）└── README.md

- **Sentence Transformers** `5.1.2` - 文本向量化```

  - 模型：`paraphrase-multilingual-MiniLM-L12-v2`

- **ChromaDB** `1.3.4` - 向量数据库## 🚀 快速开始



### 数据库### 1. 克隆项目

- **SQLite** - 轻量级关系型数据库

- **SQLAlchemy** `2.0.44` - ORM 框架```bash

- **aiosqlite** `0.21.0` - 异步 SQLite 驱动git clone <your-repo-url>

cd recommend

### 数据处理```

- **Pydantic** `2.12.4` - 数据验证

- **NumPy** `2.3.4` - 数值计算### 2. 安装依赖

- **Pandas** (可选) - 数据分析

```bash

### 前端pip install -r requirements.txt

- 纯 **HTML5 + CSS3 + JavaScript**```

- 无框架依赖，轻量快速

- Fetch API 异步请求### 3. 配置环境变量



### 开发工具复制 `.env.example` 到 `.env` 并填入你的DeepSeek API密钥：

- **pytest** - 单元测试

- **python-dotenv** - 环境变量管理```bash

- **httpx** - 异步 HTTP 客户端DEEPSEEK_API_KEY=your_api_key_here

DEEPSEEK_API_BASE=https://api.deepseek.com

---```



## 🚀 快速开始### 4. 初始化数据库



### 前置要求```bash

python -m app.database.vector_db init

- Python 3.12 或更高版本```

- DeepSeek API 密钥（[获取地址](https://platform.deepseek.com)）

- Git### 5. 运行服务



### 安装步骤```bash

uvicorn app.main:app --reload

#### 1. 克隆仓库```



```bash访问 http://localhost:8000/docs 查看API文档

git clone https://github.com/你的用户名/xjtlu-food-recommendation.git

cd xjtlu-food-recommendation## 📖 API使用示例

```

### 获取推荐

#### 2. 创建虚拟环境

```bash

**Windows:**POST /api/recommend

```cmd{

python -m venv venv  "user_id": "user123",

venv\Scripts\activate.bat  "preferences": {

```    "goal": "减脂",

    "calories_limit": 1500,

**Linux/macOS:**    "dietary_restrictions": ["无辣"]

```bash  },

python3 -m venv venv  "meal_type": "午餐"

source venv/bin/activate}

``````



#### 3. 安装依赖### 记录饮食历史



```bash```bash

pip install -r requirements.txtPOST /api/user/history

```{

  "user_id": "user123",

#### 4. 配置环境变量  "food_item": "鸡胸肉沙拉",

  "canteen": "食堂一",

复制 `.env.example` 为 `.env` 并填入你的配置：  "rating": 5

}

```bash```

cp .env.example .env

```## 🔒 伦理与隐私



编辑 `.env` 文件：- 用户数据本地存储，不上传第三方

- RAG确保推荐基于真实数据，避免幻觉

```env- 透明的推荐理由

# DeepSeek API Configuration- 支持数据导出和删除

DEEPSEEK_API_KEY=你的API密钥

DEEPSEEK_API_BASE=https://api.deepseek.com## 📝 License

DEEPSEEK_MODEL=deepseek-chat

MIT License

# Application Settings

APP_NAME=XJTLU Food Recommendation System## 🤝 贡献

APP_VERSION=1.0.0

DEBUG=True欢迎提交Issue和Pull Request！

```

#### 5. 初始化数据库

```bash
python init_db.py
```

#### 6. 启动服务器

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

或者直接运行启动脚本：

**Windows:**
```cmd
start_server.bat
```

**Linux/macOS:**
```bash
./start_server.sh
```

#### 7. 访问应用

打开浏览器访问：**http://127.0.0.1:8000**

---

## 📚 使用指南

### 获取食物推荐

1. 访问首页
2. 填写个人信息：
   - 选择健康目标（减脂/增肌/均衡饮食）
   - 设置每日卡路里目标
   - 填写饮食限制和过敏信息
3. 选择餐次（早餐/午餐/晚餐/加餐）
4. 点击"获取推荐"

### 与 AI 营养师对话

1. 滚动到页面底部的"AI 聊天助手"
2. 输入你的问题，例如：
   - "推荐一些减脂餐"
   - "中心食堂有什么健康的选择？"
   - "我想增肌，应该吃什么？"
3. AI 会根据系统中的真实菜单数据给出建议

### 管理食堂菜单

使用管理工具添加新菜品：

```bash
python manage_menu.py add
```

批量导入 JSON 数据：

```bash
python manage_menu.py import data/canteens/menu.json
```

---

## 🗂️ 项目结构

```
xjtlu-food-recommendation/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 应用入口
│   ├── config.py               # 配置管理
│   ├── api/                    # API 路由
│   │   ├── __init__.py
│   │   ├── recommend.py        # 推荐接口
│   │   ├── user.py            # 用户接口
│   │   └── chat.py            # 聊天接口
│   ├── models/                 # 数据模型
│   │   ├── __init__.py
│   │   ├── food.py
│   │   └── user.py
│   ├── database/               # 数据库
│   │   ├── __init__.py
│   │   ├── vector_db.py       # ChromaDB 向量数据库
│   │   └── user_db.py         # SQLite 用户数据库
│   └── services/               # 业务逻辑
│       ├── __init__.py
│       ├── deepseek_service.py # DeepSeek AI 服务
│       ├── rag_service.py      # RAG 检索服务
│       └── recommendation.py   # 推荐算法
├── static/                     # 前端静态文件
│   ├── index.html
│   └── RAG_GUIDE.html
├── data/                       # 数据文件
│   ├── chroma_db/             # 向量数据库存储
│   ├── users.db               # SQLite 数据库
│   └── canteens/              # 食堂菜单数据
│       └── sample_menu.json
├── tests/                      # 测试文件
├── docs/                       # 文档
├── .env                        # 环境变量（不提交到 Git）
├── .env.example               # 环境变量模板
├── .gitignore                 # Git 忽略文件
├── requirements.txt           # Python 依赖
├── init_db.py                 # 数据库初始化脚本
├── manage_menu.py             # 菜单管理工具
├── start_server.bat           # Windows 启动脚本
└── README.md                  # 项目说明
```

---

## 🧪 测试

运行单元测试：

```bash
pytest tests/
```

测试推荐功能：

```bash
python test_recommendation.py
```

---

## 📦 部署

### 使用 Docker

```dockerfile
# Dockerfile 示例
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

构建并运行：

```bash
docker build -t xjtlu-food-rec .
docker run -p 8000:8000 --env-file .env xjtlu-food-rec
```

### 部署到云平台

支持部署到：
- **Render.com** - 免费额度，配置文件已包含
- **Railway** - 快速部署
- **Vercel** - 前端托管
- **Heroku** - 传统选择

详见 [DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## 🔐 环境变量说明

| 变量名 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | - | ✅ |
| `DEEPSEEK_API_BASE` | DeepSeek API 地址 | `https://api.deepseek.com` | ❌ |
| `DEEPSEEK_MODEL` | 使用的模型名称 | `deepseek-chat` | ❌ |
| `APP_NAME` | 应用名称 | `XJTLU Food Recommendation` | ❌ |
| `DEBUG` | 调试模式 | `False` | ❌ |
| `TEMPERATURE` | AI 温度参数 | `0.7` | ❌ |

---

## 🤝 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范

- 遵循 PEP 8 Python 代码风格
- 为新功能添加测试
- 更新相关文档

---

## 📝 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 👥 作者

**项目作者** - [badger](https://github.com/yangbadger222)

---

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 优秀的 Web 框架
- [DeepSeek](https://deepseek.com/) - 强大的 AI 模型
- [ChromaDB](https://www.trychroma.com/) - 向量数据库
- [Sentence Transformers](https://www.sbert.net/) - 文本嵌入模型
- 西交利物浦大学 - 项目灵感来源

---

## 📧 联系方式

- 项目 Issues: [GitHub Issues](https://github.com/yangbadger222/xjtlu-food-recommendation/issues)
- 邮箱: yangbadger222@gmail.com

---

## 🗺️ 路线图

### v1.0.0 (当前版本)
- ✅ 基础推荐功能
- ✅ AI 聊天助手
- ✅ RAG 检索系统
- ✅ 用户偏好管理

### v1.1.0 (计划中)
- [ ] 添加更多食堂数据
- [ ] 膳食计划生成
- [ ] 营养报告导出
- [ ] 用户社区功能

### v2.0.0 (未来)
- [ ] 移动端 App
- [ ] 图像识别识别食物
- [ ] 智能手环数据集成
- [ ] 多语言支持

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个 Star！⭐**

Made with ❤️ for XJTLU Students

</div>
