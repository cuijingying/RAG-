# 培养方案智能问答系统

基于 RAG 技术的硕士研究生培养方案智能问答系统，支持自然语言查询课程信息、学分要求、修读规则等。

## 📋 项目概述

本项目是上海财经大学《非结构化数据处理》课程期末作业，基于 LangChain + Chroma + DeepSeek + Streamlit 技术栈开发的 RAG（检索增强生成）问答系统。

**核心功能**：
- 支持自然语言查询培养方案相关信息
- 基于向量数据库的语义检索
- 实时流式问答响应
- 友好的 Streamlit 交互界面

**数据源**：`program.md` - 上海财经大学软件工程专业硕士研究生培养方案（2025版）

## 🛠️ 技术栈

- **RAG 框架**：LangChain
- **向量数据库**：Chroma（本地存储）
- **LLM API**：DeepSeek API（兼容 OpenAI 接口）
- **前端界面**：Streamlit
- **文档处理**：MarkdownHeaderTextSplitter
- **容器化**：Docker

## 📦 环境配置

### 1. 创建并激活 Conda 环境

```bash
# 使用现有的 lab 环境
conda activate lab
```

### 2. 安装依赖包

```bash
pip install -r requirements.txt
```

或者使用单行命令安装所有依赖：

```bash
pip install streamlit>=1.28.0 langchain>=0.1.0 langchain-community>=0.0.10 chromadb>=0.4.0 openai>=1.0.0 python-dotenv>=1.0.0 markdown>=3.5.0 requests>=2.31.0 sentence-transformers>=2.2.0
```

### 3. 配置 DeepSeek API Key

创建 `.env` 文件：

```bash
touch .env
```

在 `.env` 文件中添加你的 DeepSeek API Key：

```env
DEEPSEEK_API_KEY=your_api_key_here
DEPLSEEK_BASE_URL=https://api.deepseek.com
```

## 🚀 快速开始

### 第 1 步：构建向量数据库

首次运行前，需要将培养方案文档导入向量数据库：

```bash
python ingest.py
```

这将在 `./chroma_db` 目录下创建本地向量数据库。

### 第 2 步：启动 Streamlit 应用

```bash
streamlit run app.py
```

应用将在浏览器中自动打开（默认地址：http://localhost:8501）

## 📁 项目结构

```
training_program/
├── program.md              # 培养方案数据源
├── project.md              # 项目要求文档
├── streamlit.md            # Streamlit 模板代码
├── requirements.txt        # Python 依赖包
├── README.md              # 项目说明文档
├── .env                   # 环境变量配置（需手动创建）
├── ingest.py              # 向量数据库构建脚本
├── app.py                 # Streamlit 主应用
├── Dockerfile             # Docker 容器化配置
└── chroma_db/             # 向量数据库存储目录（自动生成）
```

## 💡 使用示例

**查询示例**：
- "这个专业需要修多少学分？"
- "第一学期有哪些必修课？"
- "统计理论与方法这门课多少学分？"
- "选择性必修课有哪些？"
- "毕业有什么要求？"

## 🐳 Docker 部署

### 构建镜像

```bash
docker build -t rag-qa-system .
```

### 运行容器

```bash
docker run -p 8501:8501 --env-file .env rag-qa-system
```

## 📊 项目特点

1. **语义检索**：基于向量嵌入的智能检索，支持模糊查询
2. **流式响应**：实时显示 AI 回答，提升用户体验
3. **本地存储**：Chroma 向量数据库本地化，无需外部服务
4. **模块化设计**：清晰的项目结构，易于维护和扩展
5. **容器化部署**：支持 Docker 一键部署

## 🎯 核心算法

本项目应用了以下课程核心算法：

1. **文档切片**：使用 `MarkdownHeaderTextSplitter` 按二级标题（##）进行结构化切片
2. **向量嵌入**：基于 `sentence-transformers` 生成文本向量表示
3. **相似度检索**：在 Chroma 向量数据库中进行语义相似度搜索
4. **检索增强生成（RAG）**：结合检索到的上下文与大模型生成准确回答

## ⚠️ 注意事项

1. 首次运行前必须先执行 `ingest.py` 构建向量数据库
2. 确保 `.env` 文件中配置了正确的 DeepSeek API Key
3. 向量数据库 `chroma_db` 目录会在首次运行后自动生成
4. 如需更新知识库，重新运行 `ingest.py` 即可

## 👥 开发团队

- 开发环境：conda lab
- 项目周期：2025年6月
- 课程：《非结构化数据处理》期末 Project

## 📄 交付清单

- [x] 可运行代码仓库
- [x] README.md 环境配置文档
- [x] requirements.txt 依赖清单
- [x] Dockerfile 容器化配置
- [x] 技术报告（单独文档）
- [x] 向量数据库构建脚本（ingest.py）
- [x] Streamlit 问答应用（app.py）# RAG-
