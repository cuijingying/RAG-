

## 第三步：编写 Streamlit 前端应用代码

我们将使用 Colab 的 `%%writefile` 魔法命令直接在当前目录下生成一个 `app.py` 文件。新建一个代码块并运行：

```python
%%writefile app.py
import streamlit as st
import requests
import json

st.title("My Very Own Chatbot 💬")
st.caption("A Streamlit chatbot powered by Ollama on Google Colab")

# 侧边栏可以加上你的名字或者自定义图片
st.sidebar.title("设置")
name = st.sidebar.text_input("What's your name?", "User")
st.sidebar.markdown("---")
st.sidebar.write("模型正在使用: llama3")

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 接收用户输入
if prompt := st.chat_input("How can I help you?"):
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 向本地 Ollama 接口发送请求
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # 这里的 URL 指向 Colab 本地的 Ollama 服务
        url = "http://localhost:11434/api/generate"
        data = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()["response"]
            message_placeholder.markdown(result)
            st.session_state.messages.append({"role": "assistant", "content": result})
        else:
            message_placeholder.error("Error communicating with Ollama")
```

