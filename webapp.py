#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Stylist4deepseek - Web应用界面
提供基于Web的穿搭顾问交互界面
"""

from flask import Flask, render_template, request, jsonify
import os
import sys
import json
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 导入我们的穿搭推荐模块
from stylist_app import load_file_content, create_prompt, generate_outfit_recommendation

app = Flask(__name__)

# 确保templates目录存在
if not os.path.exists('templates'):
    os.makedirs('templates')

# 创建简单的HTML模板
@app.route('/create_template')
def create_template():
    # 从环境变量获取默认值
    use_api_default = os.environ.get("USE_DEEPSEEK_API", "").lower() in ['true', '1', 'yes']
    
    html_content = r"""
<!DOCTYPE html>
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
            max-width: 800px;
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
        .toggle-container {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        .toggle-container label {
            display: inline;
            margin-right: 10px;
        }
        .toggle {
            position: relative;
            display: inline-block;
            width: 60px;
            height: 34px;
        }
        .toggle input {
            opacity: 0;
            width: 0;
            height: 0;
        }
        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: .4s;
            border-radius: 34px;
        }
        .slider:before {
            position: absolute;
            content: "";
            height: 26px;
            width: 26px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
        }
        input:checked + .slider {
            background-color: #2196F3;
        }
        input:checked + .slider:before {
            transform: translateX(26px);
        }
        .settings {
            margin-top: 20px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background-color: #f8f9fa;
        }
        .settings h3 {
            margin-top: 0;
            margin-bottom: 15px;
        }
        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Stylist4deepseek<br><small>个性化穿搭推荐</small></h1>
        
        <div class="toggle-container">
            <label for="settings-toggle">高级设置:</label>
            <label class="toggle">
                <input type="checkbox" id="settings-toggle">
                <span class="slider"></span>
            </label>
        </div>
        
        <div class="settings hidden" id="settings-panel">
            <h3>API设置</h3>
            <div class="form-group">
                <label for="api-key">Deepseek API密钥:</label>
                <input type="password" id="api-key" placeholder="输入您的API密钥">
            </div>
            <div class="toggle-container">
                <label for="use-api">使用Deepseek API:</label>
                <label class="toggle">
                    <input type="checkbox" id="use-api" USEAPI_CHECKED>
                    <span class="slider"></span>
                </label>
            </div>
            <p style="font-size: 0.9em; color: #666;">
                如果不使用API，将使用示例回答。使用API需要提供有效的密钥。
            </p>
        </div>
        
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
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>正在为您生成穿搭方案...</p>
        </div>
        
        <div class="result" id="result" style="display:none;"></div>
    </div>

    <script>
        document.getElementById('settings-toggle').addEventListener('change', function() {
            const settingsPanel = document.getElementById('settings-panel');
            if (this.checked) {
                settingsPanel.classList.remove('hidden');
            } else {
                settingsPanel.classList.add('hidden');
            }
        });
        
        // 如果默认使用API，自动打开设置面板
        SETTINGS_PANEL_SCRIPT
        
        document.getElementById('submit').addEventListener('click', function() {
            const scenario = document.getElementById('scenario').value;
            const query = document.getElementById('query').value;
            const useApi = document.getElementById('use-api').checked;
            const apiKey = document.getElementById('api-key').value;
            const resultElement = document.getElementById('result');
            const loadingElement = document.getElementById('loading');
            
            // 显示加载动画
            loadingElement.style.display = 'block';
            resultElement.style.display = 'none';
            
            // 发送请求到后端
            fetch('/get_recommendation', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    scenario: scenario,
                    query: query,
                    use_api: useApi,
                    api_key: apiKey
                }),
            })
            .then(response => response.json())
            .then(data => {
                // 隐藏加载动画，显示结果
                loadingElement.style.display = 'none';
                
                // 处理结果文本，高亮显示[衣橱已有]和[建议购买]标签
                const recommendation = data.recommendation;
                const formattedText = recommendation
                    .replace(/\[衣橱已有\]/g, '<mark class="existing">[衣橱已有]</mark>')
                    .replace(/\[建议购买\]/g, '<mark class="recommended">[建议购买]</mark>');
                
                resultElement.innerHTML = formattedText;
                resultElement.style.display = 'block';
            })
            .catch((error) => {
                loadingElement.style.display = 'none';
                resultElement.textContent = '获取穿搭建议时出错，请稍后再试。';
                resultElement.style.display = 'block';
                console.error('Error:', error);
            });
        });
    </script>
</body>
</html>
    """
    
    # 根据环境变量替换模板中的占位符
    if use_api_default:
        html_content = html_content.replace('USEAPI_CHECKED', 'checked')
        html_content = html_content.replace('SETTINGS_PANEL_SCRIPT', 'document.getElementById("settings-toggle").checked = true;\ndocument.getElementById("settings-panel").classList.remove("hidden");')
    else:
        html_content = html_content.replace('USEAPI_CHECKED', '')
        html_content = html_content.replace('SETTINGS_PANEL_SCRIPT', '// No default API usage')
    
    # 写入HTML模板到静态文件
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return "模板创建成功！"

# 主页路由
@app.route('/')
def index():
    # 如果模板不存在，先创建
    if not os.path.exists('templates/index.html'):
        create_template()
    return render_template('index.html')

# API端点，处理穿搭建议请求
@app.route('/get_recommendation', methods=['POST'])
def get_recommendation():
    try:
        data = request.get_json()
        scenario = data.get('scenario', '')
        query = data.get('query', '')
        use_api = data.get('use_api', False)
        api_key = data.get('api_key', '').strip() or os.environ.get("DEEPSEEK_API_KEY", "").strip()
        
        print(f"\nWeb API请求:")
        print(f"- 场景: {scenario}")
        print(f"- 查询: {query}")
        print(f"- 使用API: {use_api}")
        if api_key:
            masked_key = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:] if len(api_key) > 8 else "***"
            print(f"- API密钥: {masked_key} (长度: {len(api_key)})")
        else:
            print("- API密钥: 未提供")
        
        # 组合用户查询
        full_query = f"场景：{scenario}\n具体需求：{query}"
        
        # 加载必要文件
        body_data = load_file_content('body_data.md')
        wardrobe_data = load_file_content('wardrobe.md')
        weather_data = load_file_content('weather_forecast.md')
        stylist_template = load_file_content('fashion_stylist_agent.md')
        
        if not all([body_data, wardrobe_data, weather_data, stylist_template]):
            return jsonify({"error": "无法加载所需数据文件。"}), 500
        
        # 创建提示词
        prompt = create_prompt(full_query, body_data, wardrobe_data, weather_data, stylist_template)
        
        # 生成穿搭建议
        recommendation = generate_outfit_recommendation(prompt, use_api=use_api, api_key=api_key)
        
        print("穿搭建议生成成功，长度:", len(recommendation))
        return jsonify({"recommendation": recommendation})
        
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