#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Deepseek API 客户端
用于与Deepseek大语言模型API进行交互
"""

import os
import json
import requests
from typing import Dict, Any, Optional, Iterator, Generator

class DeepseekClient:
    """Deepseek API 客户端类"""
    
    def __init__(self, api_key: Optional[str] = None, api_base: str = "https://api.deepseek.com/v1"):
        """
        初始化Deepseek API客户端
        
        参数:
            api_key: Deepseek API密钥，如果为None则尝试从环境变量获取
            api_base: API基础URL
        """
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
        if not self.api_key:
            print("警告: 未提供Deepseek API密钥，请通过参数或环境变量DEEPSEEK_API_KEY设置")
        else:
            # 检查并清理API密钥格式
            self.api_key = self.api_key.strip()  # 移除可能的空格
            print(f"API密钥设置成功，长度: {len(self.api_key)}")
        
        self.api_base = api_base
        
        # 设置请求头
        self.headers = {
            "Content-Type": "application/json"
        }
        
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
            print("认证头部已设置")
        else:
            print("警告: 未设置认证头部")
    
    def generate_completion(self, prompt: str, model: str = "deepseek-chat", max_tokens: int = 2000, 
                          temperature: float = 0.7) -> Dict[Any, Any]:
        """
        生成文本完成
        
        参数:
            prompt: 提示词
            model: 模型名称
            max_tokens: 最大生成的令牌数
            temperature: 温度参数，控制随机性
            
        返回:
            API响应的JSON对象
        """
        endpoint = f"{self.api_base}/chat/completions"
        
        # 打印API密钥信息（注意：生产环境应移除）
        if self.api_key:
            masked_key = self.api_key[:4] + "*" * (len(self.api_key) - 8) + self.api_key[-4:]
            print(f"使用API密钥: {masked_key}")
            print(f"API密钥长度: {len(self.api_key)}")
        else:
            print("警告: 未设置API密钥")
        
        # 打印请求信息
        print(f"请求API端点: {endpoint}")
        print(f"使用模型: {model}")
        print(f"最大令牌数: {max_tokens}")
        print(f"温度参数: {temperature}")
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            print("正在发送API请求...")
            response = requests.post(endpoint, headers=self.headers, json=payload)
            
            print(f"收到响应状态码: {response.status_code}")
            if response.status_code != 200:
                print(f"响应内容: {response.text}")
                
            response.raise_for_status()  # 检查HTTP错误
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API请求错误: {str(e)}")
            if hasattr(e, 'response') and e.response:
                print(f"响应内容: {e.response.text}")
            return {"error": str(e)}
    
    def chat_stream(self, prompt: str, model: str = "deepseek-chat", max_tokens: int = 2000,
                   temperature: float = 0.7, top_p: float = 0.9) -> Generator[str, None, None]:
        """
        生成流式文本完成，逐字返回生成内容
        
        参数:
            prompt: 提示词
            model: 模型名称
            max_tokens: 最大生成的令牌数
            temperature: 温度参数，控制随机性
            top_p: 核采样参数
            
        返回:
            一个生成器，逐字产生生成的文本内容
        """
        endpoint = f"{self.api_base}/chat/completions"
        
        # 打印API密钥信息（调试用）
        if self.api_key:
            masked_key = self.api_key[:4] + "*" * (len(self.api_key) - 8) + self.api_key[-4:]
            print(f"使用API密钥(流式): {masked_key}")
            print(f"API密钥长度: {len(self.api_key)}")
        else:
            print("警告: 未设置API密钥")
        
        # 打印请求信息
        print(f"请求流式API端点: {endpoint}")
        print(f"使用模型: {model}")
        print(f"最大令牌数: {max_tokens}")
        print(f"温度参数: {temperature}")
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "stream": True  # 启用流式传输
        }
        
        try:
            print("正在发送流式API请求...")
            response = requests.post(endpoint, headers=self.headers, json=payload, stream=True)
            
            print(f"收到响应状态码: {response.status_code}")
            if response.status_code != 200:
                print(f"响应错误: {response.text}")
                raise Exception(f"API返回错误: {response.status_code} - {response.text}")
            
            # 逐行处理SSE流式响应
            for line in response.iter_lines():
                if line:
                    # 跳过"data: "前缀并解析JSON
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        line = line[6:]  # 去除"data: "前缀
                        
                        # 跳过心跳消息
                        if line == '[DONE]':
                            print("流式响应完成")
                            break
                        
                        try:
                            # 解析响应并提取内容
                            data = json.loads(line)
                            
                            if 'choices' in data and len(data['choices']) > 0:
                                choice = data['choices'][0]
                                
                                if 'delta' in choice and 'content' in choice['delta']:
                                    content = choice['delta']['content']
                                    if content:  # 跳过空内容
                                        yield content
                                
                        except json.JSONDecodeError as e:
                            print(f"JSON解析错误: {e}")
                            print(f"原始行: {line}")
                            
        except Exception as e:
            import traceback
            print(f"流式API请求错误: {str(e)}")
            print(traceback.format_exc())
            yield f"\n[API错误: {str(e)}]"
    
    def extract_completion_text(self, response: Dict[Any, Any]) -> str:
        """
        从API响应中提取生成的文本
        
        参数:
            response: API响应的JSON对象
            
        返回:
            生成的文本内容
        """
        try:
            # 打印响应结构（调试用）
            print("响应结构:")
            if isinstance(response, dict):
                for key in response.keys():
                    print(f" - 包含键: {key}")
            else:
                print(f" - 响应不是字典类型，而是: {type(response)}")
                
            # 检查错误
            if "error" in response:
                return f"错误: {response['error']}"
            
            # Deepseek API响应解析 (通常是choices.0.message.content格式)
            if "choices" in response and len(response["choices"]) > 0:
                choice = response["choices"][0]
                print(" - 找到choices数组")
                
                if "message" in choice:
                    message = choice["message"]
                    print(" - 找到message对象")
                    
                    if "content" in message:
                        content = message["content"]
                        print(" - 找到content内容")
                        return content
                    else:
                        print(" - message中没有content字段")
                        return f"API响应错误: message中没有content字段\n{json.dumps(message, ensure_ascii=False, indent=2)}"
                elif "text" in choice:
                    # 兼容可能的老版本API
                    print(" - 找到text字段 (旧版API)")
                    return choice["text"]
                else:
                    print(" - 无法在choice中找到message或text字段")
                    return f"API响应错误: 无法解析choices内容\n{json.dumps(choice, ensure_ascii=False, indent=2)}"
            
            # 完全不符合预期的响应结构
            print("警告: 响应结构不符合预期")
            return f"无法提取生成内容，响应结构不符合预期:\n{json.dumps(response, ensure_ascii=False, indent=2)}"
            
        except Exception as e:
            import traceback
            print(f"解析响应时出错: {str(e)}")
            print(traceback.format_exc())
            return f"提取内容时出错: {str(e)}"

# 简单的使用示例
if __name__ == "__main__":
    client = DeepseekClient()
    response = client.generate_completion("请给我一个简单的穿搭建议")
    text = client.extract_completion_text(response)
    print(text) 