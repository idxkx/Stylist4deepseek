# Stylist4deepseek - 个性化穿搭推荐AI助手

## 项目简介

Stylist4deepseek 是一个基于 deepseek 大语言模型的个性化穿搭推荐助手，能够根据用户的个人信息（体型、喜好）、衣橱数据、天气情况等因素，提供专业的穿搭建议。该系统通过专业穿搭知识和个性化数据的结合，为用户提供最适合的日常穿搭方案。

## 功能特点

- **个性化穿搭推荐**：根据用户的体型特征、风格喜好和衣橱现有单品提供穿搭建议
- **衣橱内外单品推荐**：清晰标识哪些单品来自用户现有衣橱、哪些是建议购买的新品，并提供购买理由和预算建议
- **场景化推荐**：针对不同场合（工作、休闲、约会等）提供合适的穿搭方案
- **季节适应**：考虑当前天气情况，推荐合适的季节性穿搭
- **体型优化**：根据用户体型特点，推荐能够提升整体比例的穿搭组合
- **专业解析**：提供穿搭建议的专业理论依据和实用建议
- **Deepseek API集成**：支持通过Deepseek大语言模型API生成智能穿搭方案

## 项目结构

```
Stylist4deepseek/
├── README.md              # 项目说明文档
├── INSTALL.md             # 安装与使用指南
├── API_INTEGRATION.md     # Deepseek API集成指南
├── requirements.txt       # Python依赖文件
├── .env.template          # 环境变量模板
├── stylist_app.py         # 命令行应用主程序
├── webapp.py              # Web应用主程序
├── deepseek_client.py     # Deepseek API客户端
├── fashion_stylist_agent.md  # 穿搭设计师Agent提示词
├── body_data.md           # 用户个人信息
├── wardrobe.md            # 用户衣橱内衣物信息
├── weather_forecast.md    # 当前天气信息
└── templates/             # Web应用模板目录
    └── index.html         # Web应用前端页面
```

## 数据文件说明

本系统使用以下文件作为穿搭推荐的输入：

1. **fashion_stylist_agent.md** - 穿搭设计师Agent提示词，设定AI的身份和技能
2. **body_data.md** - 用户个人信息，包括身材特点、风格喜好和消费习惯等
3. **wardrobe.md** - 用户衣橱内衣物信息，作为穿搭推荐的选择范围
4. **weather_forecast.md** - 当前天气信息，用于季节性穿搭参考

## 实现方式

本项目采用以下技术实现：

1. **命令行应用**：使用Python实现的简单CLI，允许用户通过命令行进行交互
2. **Web应用**：使用Flask框架实现的轻量级Web界面，提供友好的用户交互体验
3. **AI模型**：基于提示词工程，将用户需求、个人信息、衣橱数据和天气情况等组合成高质量的提示词，交给deepseek大语言模型进行处理
4. **API集成**：支持通过Deepseek API获取专业穿搭建议，能够根据实际情况智能推荐

穿搭推荐遵循以下流程：
1. 接收用户场景需求（如工作、约会等）
2. 结合用户个人特征（体型、风格喜好）
3. 分析天气情况（温度、天气状况）
4. 从用户衣橱中选择最适合的单品组合
5. 生成完整的穿搭方案，包括单品组合、穿搭理由和实用建议

## 使用方法

使用 Stylist4deepseek 获取穿搭建议只需遵循以下步骤：

### 命令行方式

```bash
# 直接运行并等待输入穿搭需求
python stylist_app.py

# 或者直接在命令行中提供需求
python stylist_app.py --query "我今天要参加一个重要的商务会议，需要正式但不过于严肃的穿搭"

# 使用Deepseek API生成更智能的穿搭建议
python stylist_app.py --query "我今天要参加一个重要的商务会议" --use-api --api-key YOUR_API_KEY
```

### Web应用方式

1. 启动Web应用：`python webapp.py`
2. 浏览器访问：http://localhost:5000
3. 选择场景并填写具体需求
4. 可选：在高级设置中配置Deepseek API
5. 点击"获取穿搭建议"按钮

## Deepseek API集成

Stylist4deepseek支持通过Deepseek API生成更智能、更个性化的穿搭建议。使用API前需要完成以下步骤：

1. 获取Deepseek API密钥（[详细说明](API_INTEGRATION.md)）
2. 配置API密钥（环境变量、命令行参数或Web界面）
3. 启用API使用（通过参数`--use-api`或Web界面设置）

详细的API集成说明请参考[API_INTEGRATION.md](API_INTEGRATION.md)文件。

## 示例对话

```
用户：今天要去参加一个重要的工作会议，需要正式但不过于严肃的穿搭建议
AI：[提供基于用户衣橱的正式商务穿搭建议]

用户：周末约会想要显得温柔有气质，有什么推荐？
AI：[提供适合约会场合的柔美穿搭组合]
```

## 项目规划

未来计划增加的功能：

1. **穿搭图片生成**：将文字穿搭建议转化为可视化图片
2. **服饰购买推荐**：根据衣橱缺失单品提供购物建议
3. **穿搭历史记录**：记录并学习用户喜好，提升推荐准确度
4. **季节性衣橱整理建议**：根据季节变化给出衣橱整理建议
5. **多用户支持**：支持多用户配置文件，满足家庭成员不同需求
6. **高级AI模型支持**：添加对更多AI模型的支持，如GPT-4等

## 安装与配置

详细的安装与配置说明请参考 [INSTALL.md](INSTALL.md) 文件。

## 使用限制

- 系统基于现有衣橱单品进行推荐，推荐结果受限于用户输入的衣橱数据
- 天气数据需要定期更新以确保推荐的时效性
- 对于特殊场合或极端天气情况，可能需要用户提供额外信息
- 使用Deepseek API需要有效的API密钥，并可能产生API调用费用 