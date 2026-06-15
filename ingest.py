"""
向量数据库构建脚本
功能：读取 program.md，按二级标题切片，生成向量嵌入并存储到 Chroma 数据库
"""

import os
from dotenv import load_dotenv
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# 加载环境变量
load_dotenv()

def main():
    # 1. 读取 program.md 文件
    print("📖 正在读取 program.md...")
    with open("program.md", "r", encoding="utf-8") as f:
        markdown_text = f.read()

    # 2. 使用 MarkdownHeaderTextSplitter 按二级标题（##）切片
    print("✂️ 正在按二级标题切片...")
    headers_to_split_on = [
        ("##", "Header 2")
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    docs = markdown_splitter.split_text(markdown_text)

    print(f"📊 切片完成，共生成 {len(docs)} 个文档片段")

    # 3. 初始化 Embedding 模型（使用中文优化的开源模型）
    print("🧠 正在初始化 Embedding 模型（首次运行会下载模型，需要几分钟）...")
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-zh-v1.5",  # 中文语义检索效果较好的轻量级模型
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    # 4. 创建/更新 Chroma 向量数据库
    print("💾 正在构建向量数据库并存储到 ./chroma_db...")
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )

    print("✅ 向量数据库构建完成！")
    print(f"📁 数据库存储位置: {os.path.abspath('./chroma_db')}")
    print(f"📄 文档片段数量: {len(docs)}")

    # 显示切片预览
    print("\n📋 文档片段预览（前 3 个）：")
    for i, doc in enumerate(docs[:3]):
        print(f"\n--- 片段 {i+1} ---")
        print(f"元数据: {doc.metadata}")
        print(f"内容（前100字）: {doc.page_content[:100]}...")

if __name__ == "__main__":
    main()