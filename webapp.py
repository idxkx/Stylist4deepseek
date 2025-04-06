#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Stylist4deepseek - Web应用界面
提供基于Web的穿搭顾问交互界面
"""

from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import os
import sys
import json
import time
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 导入我们的穿搭推荐模块
from stylist_app import load_file_content, create_prompt, generate_outfit_recommendation

app = Flask(__name__)

# 确保templates目录存在
if not os.path.exists('templates'):
    os.makedirs('templates')

# 用户数据加载函数
def load_users_data():
    try:
        with open('users.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载用户数据出错: {str(e)}")
        return {"users": [], "selected_user": ""}

# 用户数据保存函数
def save_users_data(data):
    try:
        with open('users.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存用户数据出错: {str(e)}")
        return False

# 加载指定用户的数据
def load_user_specific_data(user_id):
    body_data = load_file_content(f'users/{user_id}/body_data.md')
    weather_data = load_file_content(f'users/{user_id}/weather_forecast.md')
    wardrobe_data = load_file_content(f'users/{user_id}/wardrobe.md')
    
    # 如果用户特定数据不存在，使用默认数据
    if not body_data:
        body_data = load_file_content('body_data.md')
    if not weather_data:
        weather_data = load_file_content('weather_forecast.md')
    if not wardrobe_data:
        wardrobe_data = load_file_content('wardrobe.md')
    
    return {
        "body_data": body_data,
        "weather_data": weather_data,
        "wardrobe_data": wardrobe_data
    }

# 创建简单的HTML模板
@app.route('/create_template')
def create_template():
    print("\n==== 开始创建/更新HTML模板 ====")
    
    # 检查模板目录是否存在
    if not os.path.exists('templates'):
        print("创建templates目录")
        os.makedirs('templates')
    
    html_content = r"""
<!DOCTYPE html>
<!-- 此模板由create_template函数生成 - 生成时间: """ + time.strftime("%Y-%m-%d %H:%M:%S") + r""" -->
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stylist4deepseek - 个性化穿搭推荐</title>
    <style>
        body {
            font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .container {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        textarea, select, input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        button {
            background-color: #4a5568;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            display: block;
            margin: 0 auto;
        }
        button:hover {
            background-color: #2d3748;
        }
        .result {
            margin-top: 30px;
            white-space: pre-wrap;
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            border-left: 4px solid #4a5568;
            font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
            line-height: 1.6;
        }
        .result mark.existing {
            background-color: #d1f0d1;
            border-radius: 4px;
            padding: 2px 5px;
            font-weight: bold;
            color: #2c662c;
        }
        .result mark.recommended {
            background-color: #ffe6e6;
            border-radius: 4px;
            padding: 2px 5px;
            font-weight: bold;
            color: #a83e3e;
        }
        .loading {
            text-align: center;
            display: none;
            margin: 20px 0;
        }
        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            animation: spin 2s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .cursor {
            display: inline-block;
            width: 2px;
            height: 18px;
            background-color: #333;
            margin-left: 2px;
            animation: blink 1s infinite;
            vertical-align: middle;
        }
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }
        footer {
            text-align: center;
            margin-top: 30px;
            font-size: 12px;
            color: #666;
        }
        .user-profile {
            border: 1px solid #ddd;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 8px;
            background-color: #f8f9fa;
        }
        .user-info {
            margin-bottom: 15px;
        }
        .user-info h3 {
            margin-top: 0;
            margin-bottom: 10px;
            color: #4a5568;
        }
        .tabs {
            display: flex;
            border-bottom: 1px solid #ddd;
            margin-bottom: 20px;
        }
        .tab {
            padding: 10px 20px;
            cursor: pointer;
            border: 1px solid transparent;
            margin-bottom: -1px;
        }
        .tab.active {
            border: 1px solid #ddd;
            border-bottom-color: #fff;
            background-color: #fff;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        .tab-content {
            display: none;
            padding: 15px;
            border: 1px solid #ddd;
            border-top: none;
            border-bottom-left-radius: 4px;
            border-bottom-right-radius: 4px;
            max-height: 300px;
            overflow-y: auto;
        }
        .tab-content.active {
            display: block;
        }
        .flex-container {
            display: flex;
            gap: 20px;
        }
        .col-left {
            flex: 1;
        }
        .col-right {
            flex: 1;
        }
        .user-select {
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Stylist4deepseek<br><small>个性化穿搭推荐</small></h1>
        
        <div class="form-group user-select">
            <label for="user">选择用户：</label>
            <select id="user">
                <!-- 将通过JavaScript动态填充 -->
            </select>
        </div>
        
        <div class="user-profile" id="user-profile">
            <!-- 用户信息将通过JavaScript动态填充 -->
        </div>
        
        <div class="flex-container">
            <div class="col-left">
                <div class="tabs">
                    <div class="tab active" data-tab="body-data">身体数据</div>
                    <div class="tab" data-tab="weather-data">天气数据</div>
                </div>
                
                <div class="tab-content active" id="body-data">
                    <!-- 身体数据内容将通过JavaScript动态填充 -->
                </div>
                
                <div class="tab-content" id="weather-data">
                    <!-- 天气数据内容将通过JavaScript动态填充 -->
                </div>
            </div>
            
            <div class="col-right">
                <div class="form-group">
                    <label for="scenario">场景选择：</label>
                    <select id="scenario">
                        <option value="工作场合">工作场合</option>
                        <option value="约会">约会</option>
                        <option value="休闲日常">休闲日常</option>
                        <option value="重要会议">重要会议</option>
                        <option value="户外活动">户外活动</option>
                        <option value="派对">派对</option>
                        <option value="其他">其他（在需求中详述）</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="query">您的穿搭需求：</label>
                    <textarea id="query" rows="4" placeholder="请描述您需要什么场合的穿搭，有什么特殊要求..."></textarea>
                </div>
                
                <button id="submit">获取穿搭建议</button>
            </div>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>正在为您生成穿搭方案...</p>
        </div>
        
        <div class="result" id="result" style="display:none;">
            <span id="content"></span><span class="cursor" id="typing-cursor"></span>
        </div>
    </div>
    
    <footer>
        穿搭建议基于环境配置自动使用最适合的生成方式
    </footer>

    <script>
        // 全局变量存储用户数据
        let usersData = {};
        let selectedUserId = '';
        
        // 页面加载完成后初始化
        document.addEventListener('DOMContentLoaded', function() {
            // 加载用户数据
            fetchUsers();
            
            // 标签页切换功能
            document.querySelectorAll('.tab').forEach(tab => {
                tab.addEventListener('click', function() {
                    // 移除所有标签页的active类
                    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                    // 移除所有内容区的active类
                    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                    
                    // 给当前点击的标签页添加active类
                    this.classList.add('active');
                    // 激活对应的内容区
                    const tabId = this.getAttribute('data-tab');
                    document.getElementById(tabId).classList.add('active');
                });
            });
            
            // 用户选择变更事件
            document.getElementById('user').addEventListener('change', function() {
                selectedUserId = this.value;
                // 更新用户信息显示
                updateUserInfo();
                // 加载用户特定数据
                fetchUserData(selectedUserId);
            });
        });
        
        // 获取所有用户数据
        function fetchUsers() {
            fetch('/api/users')
                .then(response => response.json())
                .then(data => {
                    usersData = data;
                    // 填充用户选择下拉框
                    const userSelect = document.getElementById('user');
                    userSelect.innerHTML = '';
                    
                    data.users.forEach(user => {
                        const option = document.createElement('option');
                        option.value = user.id;
                        option.textContent = `${user.name} (${user.profession})`;
                        userSelect.appendChild(option);
                        
                        // 设置默认选中的用户
                        if (user.id === data.selected_user) {
                            option.selected = true;
                            selectedUserId = user.id;
                        }
                    });
                    
                    // 更新用户信息显示
                    updateUserInfo();
                    // 加载用户特定数据
                    fetchUserData(selectedUserId);
                })
                .catch(error => {
                    console.error('获取用户数据失败:', error);
                    alert('加载用户数据失败，请刷新页面重试');
                });
        }
        
        // 更新用户信息显示
        function updateUserInfo() {
            const user = usersData.users.find(u => u.id === selectedUserId);
            if (!user) return;
            
            const profileElement = document.getElementById('user-profile');
            profileElement.innerHTML = `
                <div class="user-info">
                    <h3>${user.name}</h3>
                    <p><strong>年龄:</strong> ${user.age}岁 | <strong>性别:</strong> ${user.gender} | <strong>职业:</strong> ${user.profession}</p>
                    <p><strong>地点:</strong> ${user.location} | <strong>体型:</strong> ${user.body_type}</p>
                    <p><strong>风格偏好:</strong> ${user.style_preference}</p>
                    <p><strong>个人简介:</strong> ${user.description}</p>
                </div>
            `;
        }
        
        // 获取用户特定数据（身体特征和天气）
        function fetchUserData(userId) {
            fetch(`/api/user-data/${userId}`)
                .then(response => response.json())
                .then(data => {
                    // 填充身体数据
                    document.getElementById('body-data').innerHTML = `<pre>${data.body_data}</pre>`;
                    // 填充天气数据
                    document.getElementById('weather-data').innerHTML = `<pre>${data.weather_data}</pre>`;
                })
                .catch(error => {
                    console.error('获取用户特定数据失败:', error);
                    alert('加载用户特定数据失败，请刷新页面重试');
                });
        }
        
        // 提交获取穿搭建议
        document.getElementById('submit').addEventListener('click', function() {
            const scenario = document.getElementById('scenario').value;
            const query = document.getElementById('query').value;
            const resultElement = document.getElementById('result');
            const contentElement = document.getElementById('content');
            const cursorElement = document.getElementById('typing-cursor');
            const loadingElement = document.getElementById('loading');
            
            // 显示加载动画
            loadingElement.style.display = 'block';
            resultElement.style.display = 'none';
            contentElement.textContent = '';
            
            // 使用fetch API的流式响应功能
            fetch('/get_recommendation', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: selectedUserId,
                    scenario: scenario,
                    query: query
                }),
            })
            .then(response => {
                // 隐藏加载动画，显示结果区域
                loadingElement.style.display = 'none';
                resultElement.style.display = 'block';
                
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                
                // 读取流式数据
                function readStream() {
                    return reader.read().then(({ value, done }) => {
                        if (done) {
                            // 流结束后的处理
                            cursorElement.style.display = 'none';
                            return;
                        }
                        
                        // 解码接收到的数据
                        const text = decoder.decode(value, { stream: true });
                        
                        try {
                            // 尝试解析JSON并提取推荐文本
                            const jsonData = JSON.parse(text);
                            if (jsonData.chunk) {
                                // 处理文本片段，添加到内容区
                                let chunk = jsonData.chunk;
                                
                                // 高亮[衣橱已有]和[建议购买]标签
                                chunk = chunk
                                    .replace(/\[衣橱已有\]/g, '<mark class="existing">[衣橱已有]</mark>')
                                    .replace(/\[建议购买\]/g, '<mark class="recommended">[建议购买]</mark>');
                                
                                contentElement.innerHTML += chunk;
                            }
                        } catch (e) {
                            // 不是有效的JSON，直接显示文本
                            contentElement.textContent += text;
                        }
                        
                        // 继续读取下一块数据
                        return readStream();
                    });
                }
                
                return readStream();
            })
            .catch((error) => {
                loadingElement.style.display = 'none';
                resultElement.style.display = 'block';
                contentElement.textContent = '获取穿搭建议时出错，请稍后再试。';
                cursorElement.style.display = 'none';
                console.error('Error:', error);
            });
        });
    </script>
</body>
</html>
    """
    
    # 写入HTML模板到静态文件
    try:
        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"模板文件创建成功！长度: {len(html_content)} 字节")
        print("==== 创建/更新HTML模板完成 ====\n")
        return "模板创建成功！"
    except Exception as e:
        print(f"创建模板文件时出错: {str(e)}")
        print("==== 创建/更新HTML模板失败 ====\n")
        return f"创建模板文件时出错: {str(e)}"

# 主页路由
@app.route('/')
def index():
    # 强制每次都重新创建模板，确保使用最新版本
    print("\n==== 访问主页，准备渲染模板 ====")
    
    try:
        # 检查模板是否存在
        template_exists = os.path.exists('templates/index.html')
        print(f"模板文件存在: {template_exists}")
        
        # 删除旧模板并创建新的
        if template_exists:
            os.remove('templates/index.html')
            print("已删除旧模板文件")
        
        # 创建新模板
        create_template()
        
        # 确认模板已创建
        template_exists = os.path.exists('templates/index.html')
        print(f"新模板文件创建状态: {template_exists}")
        
        # 渲染模板
        return render_template('index.html')
    except Exception as e:
        print(f"主页路由出错: {str(e)}")
        return f"渲染主页时出错: {str(e)}"

# 调试页面路由
@app.route('/debug')
def debug():
    return render_template('debug.html')

# API端点 - 获取所有用户列表
@app.route('/api/users')
def get_users():
    users_data = load_users_data()
    return jsonify(users_data)

# API端点 - 获取用户特定数据（身体特征和天气）
@app.route('/api/user-data/<user_id>')
def get_user_data(user_id):
    user_data = load_user_specific_data(user_id)
    return jsonify(user_data)

# API端点 - 更新选定的用户
@app.route('/api/select-user', methods=['POST'])
def select_user():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        users_data = load_users_data()
        users_data['selected_user'] = user_id
        save_users_data(users_data)
        
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 流式输出生成器函数
def generate_streaming_response(prompt, use_api):
    api_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    
    # 这里不再考虑传入的use_api参数，完全依赖环境变量
    env_use_api = os.environ.get("USE_DEEPSEEK_API", "").lower() in ['true', '1', 'yes']
    use_api = env_use_api  # 强制使用环境变量设置
    
    print(f"[DEBUG] 流式响应开始 - 使用API: {use_api}")
    
    # 立即发送一个初始化消息
    yield json.dumps({"chunk": "正在准备您的穿搭建议...\n\n"})
    time.sleep(0.5)  # 短暂延迟
    
    if use_api and api_key:
        print(f"- 使用API: {use_api} (环境变量设置)")
        if api_key:
            masked_key = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:] if len(api_key) > 8 else "***"
            print(f"- API密钥: {masked_key} (长度: {len(api_key)})")
        
        try:
            # 导入API客户端
            from deepseek_client import DeepseekClient
            client = DeepseekClient(api_key=api_key)
            
            print("正在调用Deepseek API...")
            # 调用API获取流式响应
            response_generator = client.chat_stream(
                prompt=prompt,
                temperature=0.7,
                top_p=0.9,
                max_tokens=1500
            )
            
            # 明确的生成开始标记
            yield json.dumps({"chunk": "【Deepseek AI 正在生成穿搭建议...】\n\n"})
            
            full_content = ""
            chunk_count = 0
            
            for chunk in response_generator:
                chunk_count += 1
                full_content += chunk
                print(f"[DEBUG] 接收到内容片段 #{chunk_count}: 长度={len(chunk)}")
                yield json.dumps({"chunk": chunk})
                # 小延迟使输出更自然
                time.sleep(0.05)
            
            print(f"[DEBUG] API响应生成完成，总共片段数: {chunk_count}, 总长度: {len(full_content)}")
            
            # 如果没有内容，返回提示
            if not full_content.strip():
                print("[WARNING] API返回了空内容")
                yield json.dumps({"chunk": "\n\n【API返回了空内容，正在切换到默认示例...】\n\n"})
                time.sleep(1)
                
                # 加载示例回答
                from example_responses import get_outfit_example
                example = get_outfit_example(prompt)
                
                # 分割示例回答，逐段输出
                chunks = [example[i:i+20] for i in range(0, len(example), 20)]
                for chunk in chunks:
                    yield json.dumps({"chunk": chunk})
                    time.sleep(0.02)  # 快速输出示例回答
            
        except Exception as e:
            import traceback
            print(f"[ERROR] 调用API时出错: {str(e)}")
            print(traceback.format_exc())
            # 如果API调用失败，返回错误信息
            yield json.dumps({"chunk": f"\n\n【API调用出错】: {str(e)}\n\n正在切换到默认示例..."})
            time.sleep(1)
            
            # 加载示例回答
            from example_responses import get_outfit_example
            example = get_outfit_example(prompt)
            
            # 分割示例回答，逐段输出
            chunks = [example[i:i+20] for i in range(0, len(example), 20)]
            for chunk in chunks:
                yield json.dumps({"chunk": chunk})
                time.sleep(0.02)  # 快速输出示例回答
    else:
        if not use_api:
            print("[INFO] 未启用API，使用示例回答")
            yield json.dumps({"chunk": "【使用默认示例穿搭建议】\n\n"})
        else:
            print("[WARNING] 未提供API密钥，使用示例回答")
            yield json.dumps({"chunk": "【未设置API密钥，使用默认示例】\n\n"})
        
        time.sleep(0.5)
        
        # 加载示例回答
        from example_responses import get_outfit_example
        example = get_outfit_example(prompt)
        
        # 分割示例回答，逐段输出
        chunks = [example[i:i+20] for i in range(0, len(example), 20)]
        print(f"[DEBUG] 示例回答分割为 {len(chunks)} 个部分")
        
        for i, chunk in enumerate(chunks):
            if i % 10 == 0:  # 每10个片段打印一次日志
                print(f"[DEBUG] 发送示例片段 #{i+1}/{len(chunks)}")
            yield json.dumps({"chunk": chunk})
            time.sleep(0.01)  # 快速输出示例回答
    
    # 传输完成标记
    print("[DEBUG] 流式传输完成")
    yield json.dumps({"chunk": "\n\n【穿搭建议生成完毕】"})

# API端点，处理穿搭建议请求
@app.route('/get_recommendation', methods=['POST'])
def get_recommendation():
    try:
        data = request.get_json()
        user_id = data.get('user_id', '')
        scenario = data.get('scenario', '')
        query = data.get('query', '')
        
        # 仅从环境变量获取API设置
        env_use_api = os.environ.get("USE_DEEPSEEK_API", "").lower() in ['true', '1', 'yes']
        
        print(f"\nWeb API请求:")
        print(f"- 用户ID: {user_id}")
        print(f"- 场景: {scenario}")
        print(f"- 查询: {query}")
        print(f"- 使用API: {env_use_api} (环境变量设置)")
        
        # 组合用户查询
        full_query = f"场景：{scenario}\n具体需求：{query}"
        
        # 加载用户特定数据
        user_data = load_user_specific_data(user_id)
        body_data = user_data['body_data']
        weather_data = user_data['weather_data']
        wardrobe_data = user_data['wardrobe_data']
        
        # 加载通用数据
        stylist_template = load_file_content('fashion_stylist_agent.md')
        
        if not all([body_data, wardrobe_data, weather_data, stylist_template]):
            return jsonify({"error": "无法加载所需数据文件。"}), 500
        
        # 创建提示词
        prompt = create_prompt(full_query, body_data, wardrobe_data, weather_data, stylist_template)
        
        # 返回流式响应 - 传递环境变量中的API设置，不使用前端传入的参数
        return Response(
            stream_with_context(generate_streaming_response(prompt, env_use_api)),
            content_type='application/json'
        )
        
    except Exception as e:
        import traceback
        print(f"生成穿搭建议时出错: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # 确保先创建模板
    if not os.path.exists('templates/index.html'):
        create_template()
    
    # 启动Web应用
    app.run(debug=True, host='0.0.0.0', port=5000) 