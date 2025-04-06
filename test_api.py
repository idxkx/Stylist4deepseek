#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试Deepseek API调用
"""

import sys
import argparse
from deepseek_client import DeepseekClient

def main():
    parser = argparse.ArgumentParser(description='测试Deepseek API调用')
    parser.add_argument('--api-key', type=str, help='Deepseek API密钥')
    parser.add_argument('--prompt', type=str, default="请给我一个简单的穿搭建议", help='测试提示词')
    args = parser.parse_args()
    
    api_key = args.api_key
    if not api_key:
        print("请提供API密钥进行测试：")
        api_key = input("API密钥: ").strip()
    
    if not api_key:
        print("错误: 未提供API密钥")
        return
    
    prompt = args.prompt
    
    print("\n===== 测试API调用 =====")
    print(f"提示词: {prompt}")
    
    client = DeepseekClient(api_key=api_key)
    
    print("\n----- 发送请求 -----")
    response = client.generate_completion(prompt=prompt)
    
    print("\n----- 收到响应 -----")
    if "error" in response:
        print(f"错误: {response['error']}")
    else:
        print("原始响应:")
        for key, value in response.items():
            if key != "choices":
                print(f"{key}: {value}")
            else:
                print(f"{key}: [包含回答数据]")
    
    print("\n----- 提取文本 -----")
    text = client.extract_completion_text(response)
    print(f"生成文本:\n{text}")
    
    print("\n===== 测试完成 =====")

if __name__ == "__main__":
    main() 