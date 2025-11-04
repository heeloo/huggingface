#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用.env文件管理环境变量的示例
需要先安装: pip install python-dotenv
"""

import os
from openai import OpenAI

def setup_environment():
    """设置环境变量"""
    try:
        # 尝试导入dotenv
        from dotenv import load_dotenv
        
        # 加载.env文件中的环境变量
        load_dotenv()
        
        print("✓ .env文件加载成功")
        return True
        
    except ImportError:
        print("✗ 未安装python-dotenv，请运行: pip install python-dotenv")
        return False

def get_api_key():
    """获取API密钥"""
    # 尝试从.env文件中获取API密钥
    api_key = os.environ.get("HF_API_KEY")
    
    if not api_key or api_key == "你的实际Hugging_Face_API密钥":
        print("✗ 请在.env文件中设置真实的Hugging Face API密钥")
        print("   当前.env文件内容:")
        print(f"   HF_API_KEY={api_key}")
        return None
    
    print("✓ API密钥获取成功")
    return api_key

def create_client():
    """创建OpenAI客户端"""
    api_key = get_api_key()
    
    if not api_key:
        return None
    
    try:
        client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=api_key,
        )
        print("✓ OpenAI客户端创建成功")
        return client
    except Exception as e:
        print(f"✗ 创建客户端失败: {e}")
        return None

def test_api():
    """测试API连接"""
    print("=" * 50)
    print("Hugging Face API测试 (.env方法)")
    print("=" * 50)
    
    # 设置环境
    if not setup_environment():
        return False
    
    # 创建客户端
    client = create_client()
    
    if not client:
        return False
    
    # 测试API调用
    try:
        print("正在测试API连接...")
        
        completion = client.chat.completions.create(
            model="moonshotai/Kimi-K2-Instruct-0905",
            messages=[
                {
                    "role": "user",
                    "content": "用一句话介绍人工智能。"
                }
            ],
            max_tokens=50
        )
        
        print("✓ API调用成功！")
        print(f"响应: {completion.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"✗ API调用失败: {e}")
        return False

def show_instructions():
    """显示使用说明"""
    print("\n" + "=" * 60)
    print("使用说明")
    print("=" * 60)
    print("1. 安装依赖:")
    print("   pip install python-dotenv openai")
    print("\n2. 编辑.env文件:")
    print("   打开 .env 文件，将 '你的实际Hugging_Face_API密钥' 替换为真实的API密钥")
    print("\n3. 运行测试:")
    print("   python use_dotenv.py")
    print("\n4. 获取API密钥:")
    print("   - 访问 https://huggingface.co")
    print("   - 登录 → Settings → Access Tokens")
    print("   - 创建新的token并复制")
    print("=" * 60)

if __name__ == "__main__":
    show_instructions()
    
    # 检查是否需要安装依赖
    try:
        import dotenv
        import openai
    except ImportError:
        print("\n✗ 缺少必要的依赖包")
        print("请运行: pip install python-dotenv openai")
        exit(1)
    
    # 运行测试
    success = test_api()
    
    if success:
        print("\n🎉 所有测试通过！你可以开始使用Hugging Face API了。")
    else:
        print("\n❌ 测试失败，请检查上述错误信息。")