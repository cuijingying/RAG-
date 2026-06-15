#!/bin/bash
# 培养方案智能问答系统 - 一键启动脚本

echo "========================================"
echo "🎓 培养方案智能问答系统启动"
echo "========================================"

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "⚠️  未找到 .env 文件，正在创建..."
    cp .env.example .env
    echo "✅ 已创建 .env 文件，请编辑并填入你的 DEEPSEEK_API_KEY"
    echo "   nano .env"
    exit 1
fi

# 检查向量数据库
if [ ! -d "./chroma_db" ]; then
    echo "📊 向量数据库不存在，正在构建..."
    python ingest.py
    if [ $? -ne 0 ]; then
        echo "❌ 向量数据库构建失败"
        exit 1
    fi
    echo "✅ 向量数据库构建完成"
else
    echo "✅ 向量数据库已存在"
fi

# 启动 Streamlit 应用
echo "🚀 正在启动 Streamlit 应用..."
echo "📱 访问地址: http://localhost:8501"
echo "========================================"

streamlit run app.py