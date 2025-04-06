# 安装与使用指南

## 环境准备

本项目需要Python 3.6+环境。请按照以下步骤设置环境并运行应用：

### 1. 安装依赖

```bash
# 使用pip安装所需依赖
pip install -r requirements.txt
```

### 2. 配置Deepseek API (可选)

如果您想使用Deepseek API生成更真实的穿搭建议，请按照以下步骤配置：

1. 复制环境变量模板文件
   ```bash
   cp .env.template .env
   ```

2. 编辑.env文件，填入您的Deepseek API密钥
   ```
   DEEPSEEK_API_KEY=your_actual_api_key_here
   USE_DEEPSEEK_API=true
   ```

3. 如果不想使用API，可以将USE_DEEPSEEK_API设置为false，系统将使用示例回答

您也可以在命令行中直接提供API密钥：
```bash
python stylist_app.py --api-key your_api_key --use-api
```

或在Web界面的高级设置中配置。

### 3. 检查数据文件

确保以下文件已存在并包含有效内容：
- `body_data.md` - 用户个人信息
- `wardrobe.md` - 衣橱数据
- `weather_forecast.md` - 天气数据
- `fashion_stylist_agent.md` - 穿搭顾问提示词模板

### 4. 运行命令行应用

如果你想使用命令行版本：

```bash
# 直接运行并等待输入穿搭需求
python stylist_app.py

# 或者直接在命令行中提供需求
python stylist_app.py --query "我今天要参加一个重要的商务会议，需要正式但不过于严肃的穿搭"

# 使用API运行
python stylist_app.py --query "我今天要参加一个重要的商务会议" --use-api
```

### 5. 运行Web应用

如果你想使用Web界面版本：

```bash
# 启动Web应用
python webapp.py
```

启动后，打开浏览器访问：http://localhost:5000

Web应用界面中有"高级设置"选项，可以配置是否使用API及API密钥。

## 使用新功能：衣橱内外单品推荐

Stylist4deepseek系统现在支持同时推荐用户衣橱中已有的单品和建议购买的新单品，使用方法如下：

### 命令行模式

只需正常运行应用，系统会自动启用此功能：

```bash
python stylist_app.py --query "我明天要参加一个朋友的生日聚会"
```

如果使用API，推荐结果会更加精准：

```bash
python stylist_app.py --query "我明天要参加一个朋友的生日聚会" --use-api --api-key YOUR_API_KEY
```

### Web界面模式

在web界面中，输入您的穿搭需求后，系统会自动在结果中标识衣橱已有和建议购买的单品。

### 理解输出结果

输出结果中，您会看到：

1. 每件单品后标记为`[衣橱已有]`或`[建议购买]`
2. 每件单品下有"衣橱状态"的详细说明，解释为何系统认为该单品存在或不存在于您的衣橱中
3. "购买建议"部分提供推荐购买单品的预算和选购要点
4. "总结"部分解释推荐购买单品的理由和价值

## 常见问题

**问题**：应用启动后报错"无法加载所需数据文件"。

**解决方案**：确保当前工作目录中包含所有必需的数据文件，并且文件编码为UTF-8。

**问题**：Web应用页面打不开。

**解决方案**：
1. 确认应用已成功启动，没有报错信息
2. 检查端口5000是否被其他应用占用
3. 尝试使用不同的浏览器访问

**问题**：穿搭建议生成很慢或失败。

**解决方案**：
1. 如果未使用API，系统将返回示例回答
2. 如果使用API但失败，请检查API密钥是否正确
3. 如果API调用超时，可能是网络问题，请稍后再试

**问题**：使用API时提示"未设置API密钥"。

**解决方案**：
1. 确保已创建.env文件并填写了正确的API密钥
2. 确保在命令行中使用--api-key参数或在Web界面中填写了API密钥
3. 重启应用以确保环境变量生效

## 自定义

你可以通过修改以下文件来自定义穿搭顾问：

- `body_data.md` - 更新个人信息以获取更适合的穿搭建议
- `wardrobe.md` - 更新你的衣橱信息以获取基于你实际拥有衣物的建议
- `weather_forecast.md` - 更新当前的天气信息以获取更合时宜的穿搭建议
- `deepseek_client.py` - 自定义API调用参数，如模型选择、温度等 