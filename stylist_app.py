#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Stylist4deepseek - 个性化穿搭推荐AI助手
这个脚本用于启动穿搭推荐应用，处理用户输入，并生成穿搭建议。
"""

import os
import sys
import json
import argparse
from typing import Optional
from dotenv import load_dotenv

# 导入 Deepseek API 客户端
from deepseek_client import DeepseekClient

# 加载环境变量
load_dotenv()

def load_file_content(file_path):
    """加载指定文件的内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"无法加载文件 {file_path}: {str(e)}")
        return None

def create_prompt(user_query, body_data, wardrobe_data, weather_data, stylist_template):
    """创建发送给AI模型的提示词"""
    prompt = f"""
你是一位专业的穿搭顾问，请根据以下信息为用户提供穿搭建议：

# 用户需求
{user_query}

# 用户个人信息
{body_data}

# 用户衣橱数据
{wardrobe_data}

# 天气数据
{weather_data}

# 穿搭顾问角色
{stylist_template}

请提供一套完整的穿搭方案，包括：
1. 用户衣橱内已有的单品（必须标记为"[衣橱已有]"）
2. 用户衣橱中不存在但推荐搭配的单品（必须标记为"[建议购买]"）

请仔细分析用户的衣橱数据，对于每件推荐的衣物，准确判断其是否存在于用户衣橱中。
结合用户的体型特点、个人风格喜好和当前天气情况，详细解释为什么推荐这套穿搭方案。

请使用以下格式提供穿搭建议：

【穿搭设计方案】#[编号]

▶ 场景定位：[具体场合描述]
▶ 风格基调：[主要风格定义] + [辅助风格元素]
▶ 体型优化：[针对用户体型特点的优化策略]
▶ 季节适应：[季节] | [温度范围] | [天气条件]

━━━━━━━━━━ 单品组合 ━━━━━━━━━━

➊ 上装：[品类] + [材质] + [颜色] + [剪裁特点] [衣橱已有/建议购买]
   • 亮点：[设计亮点]
   • 搭配理由：[为何选择此单品的理论依据]
   • 衣橱状态：[详细解释该单品是否存在于用户衣橱中，如果存在，请指明具体是哪件]

➋ 下装：[品类] + [材质] + [颜色] + [剪裁特点] [衣橱已有/建议购买]
   • 亮点：[设计亮点]
   • 搭配理由：[为何选择此单品的理论依据]
   • 衣橱状态：[详细解释该单品是否存在于用户衣橱中，如果存在，请指明具体是哪件]

➌ 外套：[品类] + [材质] + [颜色] + [剪裁特点]（如适用）[衣橱已有/建议购买]
   • 亮点：[设计亮点]
   • 搭配理由：[为何选择此单品的理论依据]
   • 衣橱状态：[详细解释该单品是否存在于用户衣橱中，如果存在，请指明具体是哪件]

➍ 鞋履：[品类] + [材质] + [颜色] + [设计特点] [衣橱已有/建议购买]
   • 亮点：[设计亮点]
   • 搭配理由：[为何选择此单品的理论依据]
   • 衣橱状态：[详细解释该单品是否存在于用户衣橱中，如果存在，请指明具体是哪件]

➎ 包袋：[品类] + [材质] + [颜色] + [设计特点]（如适用）[衣橱已有/建议购买]
   • 亮点：[设计亮点]
   • 搭配理由：[为何选择此单品的理论依据]
   • 衣橱状态：[详细解释该单品是否存在于用户衣橱中，如果存在，请指明具体是哪件]

➏ 配饰：[首饰/帽子/围巾等] + [材质] + [颜色] + [设计特点] [衣橱已有/建议购买]
   • 亮点：[设计亮点]
   • 搭配理由：[为何选择此单品的理论依据]
   • 衣橱状态：[详细解释该单品是否存在于用户衣橱中，如果存在，请指明具体是哪件]

━━━━━━━━━━ 穿搭解析 ━━━━━━━━━━

⚡ 色彩和谐：[色彩理论解析] | [季型匹配说明]
⚡ 比例构建：[黄金分割点应用] | [视觉重心设计]
⚡ 材质互动：[面料组合逻辑] | [质感层次打造]
⚡ 风格统一：[风格一致性保证] | [个性表达点]
⚡ 与用户喜好匹配：[详细分析此穿搭方案如何契合用户的个人风格喜好]

━━━━━━━━━━ 实用建议 ━━━━━━━━━━

✓ 穿着顺序：[穿搭的正确次序]
✓ 变体拓展：[2-3种简易变化方案，清楚标明哪些单品是衣橱已有/建议购买]
✓ 注意事项：[特殊维护要点]
✓ 购买建议：[对于推荐购买的单品，给出预算友好的购买建议]

━━━━━━━━━━ 总结 ━━━━━━━━━━

✓ 已有单品利用：[解释如何充分利用用户已有的衣物]
✓ 推荐购买理由：[解释为什么推荐购买特定单品，以及它们将如何提升整体衣橱价值]
"""
    return prompt

def generate_outfit_recommendation(prompt, use_api: bool = True, api_key: Optional[str] = None):
    """
    生成穿搭建议
    
    参数:
        prompt: 提示词
        use_api: 是否使用API，如果为False则返回示例回答
        api_key: API密钥，如果为None则从环境变量获取
    
    返回:
        穿搭建议文本
    """
    # 使用API生成回答
    if use_api:
        try:
            print(f"API使用设置: {use_api}")
            if api_key:
                masked_key = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:] if len(api_key) > 8 else "***"
                print(f"API密钥提供: {masked_key}, 长度: {len(api_key)}")
            else:
                print("未直接提供API密钥，将尝试从环境变量获取")
            
            # 初始化客户端
            client = DeepseekClient(api_key=api_key)
            
            # 检查API密钥
            if not client.api_key:
                print("警告: 未设置API密钥，将使用示例回答")
                return generate_outfit_recommendation(prompt, use_api=False)
            
            # 调用API
            print("正在调用Deepseek API生成穿搭建议...")
            response = client.generate_completion(
                prompt=prompt,
                model="deepseek-chat",  # 或其他适合的模型
                max_tokens=2000,
                temperature=0.7
            )
            
            # 提取回答文本
            recommendation = client.extract_completion_text(response)
            
            # 检查是否有错误
            if recommendation.startswith("错误:"):
                print(f"API调用出错: {recommendation}")
                print("将使用示例回答...")
                return generate_outfit_recommendation(prompt, use_api=False)
            
            print("成功获取API回答")
            return recommendation
            
        except Exception as e:
            import traceback
            print(f"调用API时出错: {str(e)}")
            print(traceback.format_exc())
            print("将使用示例回答...")
            return generate_outfit_recommendation(prompt, use_api=False)
    
    # 使用示例回答
    print("使用示例回答...")
    response = """
【穿搭设计方案】#001

▶ 场景定位：工作日通勤
▶ 风格基调：极简都市风 + 法式优雅元素
▶ 体型优化：强调腰线、平衡梨形身材比例
▶ 季节适应：春季 | 5-20℃ | 多云转晴

━━━━━━━━━━ 单品组合 ━━━━━━━━━━

➊ 上装：真丝飘带衬衫 + 优质真丝 + 浅蓝色 + 立领设计 [衣橱已有]
   • 亮点：飘带元素增添女性柔美气质
   • 搭配理由：立领修饰颈部线条，飘带可多种系法变化造型
   • 衣橱状态：用户衣橱中有一件浅蓝色真丝立领衬衫，带有可拆卸飘带，是去年购买的高质量单品

➋ 下装：高腰九分烟管裤 + 挺括面料 + 黑色 + 直筒剪裁 [衣橱已有]
   • 亮点：高腰设计拉长腿部比例
   • 搭配理由：修身但不紧绷的剪裁平衡下半身比例，黑色显瘦
   • 衣橱状态：用户衣橱中有两条高腰黑色直筒裤，选择那条九分款更适合春季穿着

➌ 外套：收腰短款西装 + 精致羊毛混纺 + 黑色 + 短款设计 [建议购买]
   • 亮点：收腰设计强调腰线
   • 搭配理由：短款西装与高腰裤搭配创造黄金比例，增添专业感
   • 衣橱状态：用户衣橱中有一件常规版型的黑色西装，但缺少收腰设计的短款西装，建议购买以更好地突出腰线

➍ 鞋履：裸色尖头高跟鞋 + 优质皮革 + 肤色 + 7cm粗跟 [衣橱已有]
   • 亮点：视觉延伸腿部线条
   • 搭配理由：粗跟设计兼顾稳定性和舒适度，肤色增加腿部延伸感
   • 衣橱状态：用户衣橱中有一双与描述完全匹配的裸色粗跟高跟鞋，状态良好

➎ 包袋：结构化通勤托特包 + 小牛皮 + 深酒红色 + 金属五金 [建议购买]
   • 亮点：专业大气，实用性强，酒红色增添高级感
   • 搭配理由：容量适中可容纳电脑，色彩为黑蓝基础搭配注入活力
   • 衣橱状态：用户衣橱中有黑色和米色托特包，但缺少能为穿搭增添色彩的款式，深酒红色是安全但有品味的选择

➏ 配饰：18K金珍珠锁骨链 + 优雅珍珠 + 金白搭配 + 简约设计 [衣橱已有]
   • 亮点：低调优雅的点缀
   • 搭配理由：珍珠元素与飘带衬衫呼应，增添女性柔美气质
   • 衣橱状态：用户珠宝盒中有一条珍珠锁骨链，为家传饰品，品质优良且具有情感价值

━━━━━━━━━━ 穿搭解析 ━━━━━━━━━━

⚡ 色彩和谐：浅蓝+黑色基础配色 | 肤色鞋履温和过渡 | 金色饰品点缀 | 酒红包袋提亮整体
⚡ 比例构建：高腰裤+短款外套应用3:7黄金比例 | 视觉重心在腰部
⚡ 材质互动：硬挺西装+柔软真丝+皮革形成质感层次 | 正式感与柔美平衡
⚡ 风格统一：都市极简为基调 | 飘带与珍珠增添法式风情 | 整体简约大气
⚡ 与用户喜好匹配：根据用户个人信息，她偏爱简约优雅的风格，且对法式元素有好感。这套穿搭使用她喜欢的蓝色系作为主色调，并通过立领、飘带等细节呼应她对精致细节的欣赏

━━━━━━━━━━ 实用建议 ━━━━━━━━━━

✓ 穿着顺序：内搭衬衫 → 高腰裤 → 短款西装 → 配饰点缀
✓ 变体拓展：
  1. 天气转暖可脱去西装，领口飘带换系法增添变化 [全部为衣橱已有]
  2. 下班约会可更换真丝裹身中长裙 [建议购买]，保留相同上装与配饰 [衣橱已有]
  3. 周末休闲版本：将上装换为白色棉质T恤 [衣橱已有]，配同色系休闲夹克 [建议购买]
✓ 注意事项：真丝衬衫避免使用普通洗衣粉，建议手洗或干洗
✓ 购买建议：
  - 收腰短款西装：建议关注季末折扣，预算2000-3000元，优先选择羊毛含量高的款式
  - 酒红色托特包：可考虑二线轻奢品牌，预算1500-2500元，注意选择结构挺括、有内部分隔的款式
  - 真丝裹身裙：建议选择可调节腰带的设计，预算800-1500元

━━━━━━━━━━ 总结 ━━━━━━━━━━

✓ 已有单品利用：本套穿搭充分利用了用户已有的高质量基础单品（真丝衬衫、高腰裤、珍珠配饰和裸色高跟鞋），这些单品都是经典款式，组合起来已具备职场优雅感
✓ 推荐购买理由：建议购买的三件单品（收腰西装、酒红包袋和真丝裹身裙）都是能够提升整体衣橱价值的投资款。收腰西装强调用户优势腰线；酒红包袋为多套穿搭增添色彩活力；真丝裹身裙则增加了下装选择，使工作-约会的场景切换更为顺畅。这三件单品都具有较高的性价比和多种搭配可能性。
"""
    return response

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Stylist4deepseek - 个性化穿搭推荐AI助手')
    parser.add_argument('--query', type=str, help='用户查询')
    parser.add_argument('--api-key', type=str, help='Deepseek API密钥')
    parser.add_argument('--use-api', action='store_true', help='使用API生成回答，而非示例回答')
    parser.add_argument('--no-api', action='store_true', help='强制不使用API，使用示例回答')
    args = parser.parse_args()
    
    # 加载必要文件
    body_data = load_file_content('body_data.md')
    wardrobe_data = load_file_content('wardrobe.md')
    weather_data = load_file_content('weather_forecast.md')
    stylist_template = load_file_content('fashion_stylist_agent.md')
    
    if not all([body_data, wardrobe_data, weather_data, stylist_template]):
        print("错误：无法加载所需数据文件。请确保所有文件都存在。")
        sys.exit(1)
    
    # 获取用户查询
    user_query = args.query if args.query else input("请描述你需要什么场合的穿搭建议: ")
    
    # 创建提示词
    prompt = create_prompt(user_query, body_data, wardrobe_data, weather_data, stylist_template)
    
    # 是否使用API - 命令行参数优先，其次是环境变量
    env_use_api = os.environ.get("USE_DEEPSEEK_API", "").lower() in ['true', '1', 'yes']
    use_api = args.use_api or (env_use_api and not args.no_api)
    
    print(f"\n配置信息:")
    print(f"- 命令行指定使用API: {args.use_api}")
    print(f"- 命令行指定不使用API: {args.no_api}")
    print(f"- 环境变量指定使用API: {env_use_api}")
    print(f"- 最终API使用设置: {use_api}")
    
    # 获取API密钥 - 命令行参数优先，其次是环境变量
    api_key = args.api_key or os.environ.get("DEEPSEEK_API_KEY")
    if api_key:
        masked_key = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:] if len(api_key) > 8 else "***"
        print(f"- API密钥: {masked_key} (长度: {len(api_key)})")
    else:
        print("- API密钥: 未提供")
    
    # 生成穿搭建议
    recommendation = generate_outfit_recommendation(prompt, use_api=use_api, api_key=api_key)
    
    # 输出结果
    print("\n==== 你的个性化穿搭建议 ====\n")
    print(recommendation)
    print("\n===========================\n")

if __name__ == "__main__":
    main() 