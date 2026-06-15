"""
培养方案智能问答系统 - Streamlit 前端应用
功能：基于 RAG 技术的自然语言问答界面
"""

import streamlit as st
from dotenv import load_dotenv
import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# 加载环境变量
load_dotenv()

# 获取 DeepSeek API 配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

# 页面配置
st.set_page_config(
    page_title="培养方案智能问答系统",
    page_icon="🎓",
    layout="wide"
)

# 初始化 Embedding 模型（缓存）
@st.cache_resource
def get_embeddings():
    """获取缓存的 Embedding 模型"""
    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-zh-v1.5",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

# 加载向量数据库（缓存）
@st.cache_resource
def load_vector_store():
    """加载缓存的向量数据库"""
    if not os.path.exists("./chroma_db"):
        st.error("❌ 向量数据库不存在！请先运行 `python ingest.py` 构建数据库。")
        st.stop()
    return Chroma(
        persist_directory="./chroma_db",
        embedding_function=get_embeddings()
    )

# 获取 LLM 模型（缓存）
@st.cache_resource
def get_llm():
    """获取缓存的 LLM 模型"""
    if not DEEPSEEK_API_KEY:
        st.error("❌ 未找到 DEEPSEEK_API_KEY！请在 .env 文件中配置。")
        st.stop()
    return ChatOpenAI(
        model="deepseek-chat",
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL,
        temperature=0.7,
        streaming=True
    )

# 构建 Prompt 模板
def create_prompt_template():
    """构建 RAG 问答的 Prompt 模板"""
    template = """你是一个专业的学术顾问，专门回答关于上海财经大学软件工程专业硕士研究生培养方案的问题。

请根据以下检索到的相关文档片段，准确回答用户的问题。

【检索到的相关文档片段】：
{context}

【用户问题】：
{question}

回答要求：
1. 基于提供的文档片段回答，不要编造信息
2. 如果文档中没有相关信息，请明确说明
3. 回答要准确、清晰、有条理
4. 可以适当引用具体的课程代码、学分、学期等信息
5. 使用友好、专业的语气

请开始回答："""
    return ChatPromptTemplate.from_template(template)

# 主界面
st.title("🎓 培养方案智能问答系统")
st.caption("基于 RAG 技术的上海财经大学软件工程硕士培养方案问答助手")

# 侧边栏
st.sidebar.title("⚙️ 系统设置")
st.sidebar.markdown("---")
st.sidebar.write(f"🤖 LLM 模型: DeepSeek-Chat")
st.sidebar.write(f"📊 向量数据库: Chroma (本地)")
st.sidebar.write(f"🧠 Embedding 模型: BAAI/bge-small-zh-v1.5")

# 检查 API Key 配置
if not DEEPSEEK_API_KEY:
    st.sidebar.error("⚠️ 未配置 DEEPSEEK_API_KEY")
    st.info("请在项目根目录创建 `.env` 文件并添加：\n```env\nDEEPSEEK_API_KEY=your_api_key\n```")

st.sidebar.markdown("---")
st.sidebar.write("📝 使用提示：")
st.sidebar.write("- 支持自然语言查询")
st.sidebar.write("- 可以问课程信息、学分要求等")
st.sidebar.write("- 例如：'第一学期有哪些必修课？'")

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 接收用户输入
if prompt := st.chat_input("💬 请输入您的问题（例如：这个专业需要修多少学分？）"):
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 生成回答
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # 1. 检索相关文档片段
            with st.spinner("🔍 正在检索相关文档..."):
                vectorstore = load_vector_store()
                retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
                docs = retriever.invoke(prompt)

                # 组装上下文
                context = "\n\n---\n\n".join([doc.page_content for doc in docs])

                # 显示检索到的文档片段（可折叠）
                with st.expander("📄 检索到的相关文档片段（点击展开）"):
                    for i, doc in enumerate(docs, 1):
                        st.markdown(f"**片段 {i}**（来源：{doc.metadata.get('Header 2', '未知')}）")
                        st.text(doc.page_content)
                        st.markdown("---")

            # 2. 构建并发送 Prompt
            with st.spinner("🤖 正在生成回答..."):
                llm = get_llm()
                prompt_template = create_prompt_template()
                formatted_prompt = prompt_template.format(context=context, question=prompt)

                # 3. 流式调用 DeepSeek API
                response = llm.stream(formatted_prompt)

                # 4. 流式显示回答
                for chunk in response:
                    if chunk.content:
                        full_response += chunk.content
                        message_placeholder.markdown(full_response + "▌")

                # 移除光标
                message_placeholder.markdown(full_response)

            # 保存到历史记录
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            error_message = f"❌ 发生错误：{str(e)}"
            message_placeholder.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})

# 清除对话按钮
if st.button("🗑️ 清除对话历史"):
    st.session_state.messages = []
    st.rerun()

# 页脚
st.markdown("---")
st.markdown("<div style='text-align: center; color: gray; font-size: 12px;'>培养方案智能问答系统 | 上海财经大学软件工程专业 | 2025版</div>", unsafe_allow_html=True)