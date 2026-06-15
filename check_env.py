#!/usr/bin/env python3
"""
环境检查脚本 - 确认所有依赖是否正确安装
"""

import sys

print("=" * 60)
print("🔍 Python 环境检查")
print("=" * 60)
print(f"Python 版本: {sys.version}")
print(f"Python 路径: {sys.executable}")
print()

# 检查关键模块
modules_to_check = [
    ("streamlit", "streamlit"),
    ("langchain", "langchain"),
    ("langchain_community", "langchain-community"),
    ("langchain_text_splitters", "langchain-text-splitters"),
    ("langchain_chroma", "langchain-chroma"),
    ("langchain_huggingface", "langchain-huggingface"),
    ("langchain_openai", "langchain-openai"),
    ("langchain_core", "langchain-core"),
    ("chromadb", "chromadb"),
    ("openai", "openai"),
    ("dotenv", "python-dotenv"),
]

print("=" * 60)
print("📦 依赖包检查")
print("=" * 60)

missing_packages = []
for module_name, package_name in modules_to_check:
    try:
        __import__(module_name)
        print(f"✅ {package_name}")
    except ImportError:
        print(f"❌ {package_name} - 未安装")
        missing_packages.append(package_name)

print()
if missing_packages:
    print("=" * 60)
    print("⚠️ 缺少的包，请运行以下命令安装：")
    print("=" * 60)
    print(f"pip install {' '.join(missing_packages)}")
else:
    print("=" * 60)
    print("✅ 所有依赖包已正确安装！")
    print("=" * 60)

print()
print("=" * 60)
print("🚀 启动指南")
print("=" * 60)
print("1. 构建向量数据库（首次运行）：")
print("   python ingest.py")
print()
print("2. 启动 Streamlit 应用：")
print("   streamlit run app.py")
print()
print("3. 浏览器访问：")
print("   http://localhost:8501")
print("=" * 60)