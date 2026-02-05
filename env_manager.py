#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
虚拟环境管理工具
用于创建和管理多个相互隔离的虚拟环境，每个环境可以有不同的依赖配置
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 虚拟环境存储目录
VENV_DIR = os.path.join(PROJECT_ROOT, "venvs")

# 环境配置模板目录
CONFIG_TEMPLATES_DIR = os.path.join(PROJECT_ROOT, "config_templates")

# 默认环境配置
DEFAULT_ENV_CONFIG = {
    "name": "default",
    "dependencies": [
        "openai>=1.0.0",
        "python-dotenv>=1.0.0"
    ],
    "description": "默认环境配置"
}

def ensure_directories():
    """确保必要的目录存在"""
    for directory in [VENV_DIR, CONFIG_TEMPLATES_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ 创建目录: {directory}")

def create_venv(env_name):
    """创建新的虚拟环境"""
    venv_path = os.path.join(VENV_DIR, env_name)
    
    if os.path.exists(venv_path):
        print(f"✗ 虚拟环境 '{env_name}' 已存在")
        return False
    
    print(f"正在创建虚拟环境 '{env_name}'...")
    
    # 创建虚拟环境
    result = subprocess.run(
        [sys.executable, "-m", "venv", venv_path],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"✗ 创建虚拟环境失败: {result.stderr}")
        return False
    
    print(f"✓ 虚拟环境 '{env_name}' 创建成功")
    return True

def install_dependencies(env_name, dependencies):
    """安装依赖到指定的虚拟环境"""
    venv_path = os.path.join(VENV_DIR, env_name)
    
    if not os.path.exists(venv_path):
        print(f"✗ 虚拟环境 '{env_name}' 不存在")
        return False
    
    # 获取pip路径
    if sys.platform == "win32":
        pip_path = os.path.join(venv_path, "Scripts", "pip.exe")
    else:
        pip_path = os.path.join(venv_path, "bin", "pip")
    
    print(f"正在为虚拟环境 '{env_name}' 安装依赖...")
    
    # 升级pip
    subprocess.run([pip_path, "install", "--upgrade", "pip"], capture_output=True)
    
    # 安装依赖
    for dependency in dependencies:
        result = subprocess.run(
            [pip_path, "install", dependency],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"✗ 安装依赖 '{dependency}' 失败: {result.stderr}")
            return False
        else:
            print(f"✓ 安装依赖 '{dependency}' 成功")
    
    print(f"✓ 所有依赖安装完成")
    return True

def create_env_config(env_name, dependencies, description=""):
    """创建环境配置文件"""
    config_path = os.path.join(CONFIG_TEMPLATES_DIR, f"{env_name}.json")
    
    import json
    config = {
        "name": env_name,
        "dependencies": dependencies,
        "description": description,
        "created_at": datetime.now().isoformat()
    }
    
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✓ 环境配置文件已保存到: {config_path}")
    return config_path

def list_envs():
    """列出所有已创建的虚拟环境"""
    if not os.path.exists(VENV_DIR):
        print("✗ 还没有创建任何虚拟环境")
        return
    
    envs = os.listdir(VENV_DIR)
    if not envs:
        print("✗ 还没有创建任何虚拟环境")
        return
    
    print("\n已创建的虚拟环境:")
    print("-" * 50)
    
    for env in envs:
        env_path = os.path.join(VENV_DIR, env)
        if os.path.isdir(env_path):
            # 检查是否有配置文件
            config_path = os.path.join(CONFIG_TEMPLATES_DIR, f"{env}.json")
            if os.path.exists(config_path):
                import json
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                print(f"✓ {env} - {config.get('description', '无描述')}")
            else:
                print(f"✓ {env} - 无配置文件")
    
    print("-" * 50)

def activate_env(env_name):
    """生成激活虚拟环境的命令"""
    venv_path = os.path.join(VENV_DIR, env_name)
    
    if not os.path.exists(venv_path):
        print(f"✗ 虚拟环境 '{env_name}' 不存在")
        return
    
    print(f"\n激活虚拟环境 '{env_name}' 的命令:")
    print("-" * 50)
    
    if sys.platform == "win32":
        activate_cmd = os.path.join(venv_path, "Scripts", "activate.bat")
        print(f"Windows: {activate_cmd}")
    else:
        activate_cmd = os.path.join(venv_path, "bin", "activate")
        print(f"Unix/Linux/Mac: source {activate_cmd}")
    
    print("-" * 50)

def create_env_from_config(env_name, config):
    """根据配置创建虚拟环境"""
    # 创建虚拟环境
    if not create_venv(env_name):
        return False
    
    # 安装依赖
    if not install_dependencies(env_name, config["dependencies"]):
        return False
    
    # 创建配置文件
    create_env_config(env_name, config["dependencies"], config["description"])
    
    print(f"\n🎉 虚拟环境 '{env_name}' 创建成功！")
    print(f"   描述: {config['description']}")
    print(f"   依赖: {', '.join(config['dependencies'])}")
    
    return True

def create_sample_envs():
    """创建示例虚拟环境"""
    print("\n创建示例虚拟环境...")
    print("-" * 50)
    
    # 创建默认环境
    default_config = {
        "name": "default",
        "dependencies": ["openai>=1.0.0", "python-dotenv>=1.0.0"],
        "description": "默认环境 - 基础Hugging Face API功能"
    }
    create_env_from_config("default", default_config)
    
    # 创建带d2l的环境
    d2l_config = {
        "name": "with_d2l",
        "dependencies": ["openai>=1.0.0", "python-dotenv>=1.0.0", "d2l"],
        "description": "包含d2l库的环境 - 用于深度学习教学"
    }
    create_env_from_config("with_d2l", d2l_config)
    
    # 创建带jupyter的环境
    jupyter_config = {
        "name": "with_jupyter",
        "dependencies": ["openai>=1.0.0", "python-dotenv>=1.0.0", "jupyter>=1.0.0", "ipython>=8.0.0"],
        "description": "包含Jupyter的环境 - 用于交互式开发"
    }
    create_env_from_config("with_jupyter", jupyter_config)
    
    print("-" * 50)
    print("示例虚拟环境创建完成！")

def main():
    """主函数"""
    print("=" * 60)
    print("虚拟环境管理器")
    print("=" * 60)
    print("管理多个相互隔离的虚拟环境，每个环境可以有不同的配置")
    print("=" * 60)
    
    # 确保必要的目录存在
    ensure_directories()
    
    # 显示菜单
    while True:
        print("\n菜单选项:")
        print("1. 创建示例虚拟环境")
        print("2. 创建自定义虚拟环境")
        print("3. 列出所有虚拟环境")
        print("4. 激活虚拟环境")
        print("5. 退出")
        
        choice = input("请选择操作 (1-5): ")
        
        if choice == "1":
            create_sample_envs()
        elif choice == "2":
            env_name = input("请输入虚拟环境名称: ")
            dependencies_input = input("请输入依赖包（用逗号分隔，例如: openai,python-dotenv）: ")
            dependencies = [dep.strip() for dep in dependencies_input.split(",")]
            description = input("请输入环境描述: ")
            
            config = {
                "name": env_name,
                "dependencies": dependencies,
                "description": description
            }
            
            create_env_from_config(env_name, config)
        elif choice == "3":
            list_envs()
        elif choice == "4":
            env_name = input("请输入要激活的虚拟环境名称: ")
            activate_env(env_name)
        elif choice == "5":
            print("退出虚拟环境管理器...")
            break
        else:
            print("✗ 无效的选择，请重试")

if __name__ == "__main__":
    main()
