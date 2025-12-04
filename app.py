import streamlit as st
import os
from dotenv import load_dotenv

# --- 1. 核心组件导入 ---
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 加载环境变量
load_dotenv()

# --- 2. 页面配置 ---
# 将页面标题和图标改为英文
st.set_page_config(page_title="Omni AI Learning Assistant", page_icon="🎓")
st.title("🎓 Omni AI Learning Assistant")

# --- 3. 状态管理 (Session State) ---
if "chat_store" not in st.session_state:
    st.session_state["chat_store"] = ChatMessageHistory()
    # 初始欢迎语 (改为英文)
    st.session_state["chat_store"].add_ai_message("Hello! I am your Omni Learning Assistant. Please select a subject to start!")

# 辅助函数：获取历史记录
def get_session_history(session_id: str):
    return st.session_state["chat_store"]

# --- 4. 侧边栏设置 (功能升级区) ---
with st.sidebar:
    st.header("⚙️ Settings")  # 设置
    
    # 4.1 学科扩展：选项改为英文
    subject = st.selectbox(
        "📚 Subject", 
        options=["Computer Science", "Mathematics", "Physics", "Biology", "Literature", "History"]
    )
    
    # 4.2 风格选择：选项改为英文
    style = st.selectbox(
        "🗣️ Teaching Style", 
        options=["Concise", "Detailed", "Socratic"]
    )
    
    # 4.3 高级设置：创造力参数 (UI改为英文)
    with st.expander("🛠️ Advanced Model Parameters"):
        temperature = st.slider(
            "Creativity (Temperature)", 
            min_value=0.0, max_value=1.0, value=0.3, step=0.1,
            help="Higher values make responses more random/creative, lower values make them more rigorous. Low for STEM, High for Humanities."
        )
    
    # 4.4 清空对话按钮 (UI改为英文)
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state["chat_store"].clear()
        # 重置后的提示语也改为英文
        st.session_state["chat_store"].add_ai_message(f"Reset successful. Let's start discussing **{subject}**!")
        st.rerun()

# --- 5. 聊天界面渲染 ---
# 遍历历史记录并显示
for msg in st.session_state["chat_store"].messages:
    role = "assistant" if msg.type == "ai" else "human"
    # 针对代码和公式优化显示
    st.chat_message(role).write(msg.content)

# --- 6. 核心逻辑 (LCEL链) ---
def get_chain(subject, style, temperature):
    # --- 1. 先获取 API Key (逻辑放在外面) ---
    # 优先尝试从本地环境变量获取
    api_key = os.getenv("OPENAI_API_KEY")
    
    # 如果本地没有，尝试从 Streamlit 云端 Secrets 获取
    if not api_key:
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
        except:
            # 如果都没有，报错并停止
            st.error("未检测到 API Key！请确保在 .env 文件(本地)或 Secrets(云端)中配置了 key。")
            st.stop()

    # --- 2. 再初始化模型 (使用刚才获取的 api_key 变量) ---
    llm = ChatOpenAI(
        api_key=api_key,  # 这里直接填变量名
        model="deepseek-chat",
        base_url="https://api.deepseek.com",
        temperature=temperature,
        streaming=True
    )

    # 6.2 风格与提示词字典 (键名必须与上方 selectbox 的英文选项一致)
    style_prompts = {
        "Concise": "Provide direct answers with minimal fluff. If it's a STEM question, list formulas and results directly.",
        "Detailed": "Teach like a patient tutor. 1. Give the direct conclusion first; 2. Break down the principles step-by-step; 3. Use real-world analogies.",
        "Socratic": "Do not give the answer directly. Guide the user to think for themselves by asking leading questions and providing hints step-by-step."
    }

    # 6.3 系统提示词 (针对物理/生物做了优化，并翻译为英文)
    # (后面的 prompt 和 chain 代码保持不变)
    
    # 6.3 系统提示词
    system_prompt = f"""You are a senior expert tutor in the field of {{subject}}.
    
    Please follow this teaching style:
    {style_prompts[style]}
    
    Guidelines:
    1. If formulas are involved, you MUST use LaTeX format (e.g., $E=mc^2$).
    2. If biology/chemical reactions are involved, clearly list the reaction equations.
    3. If code is involved, use code blocks.
    4. Sternly refuse to answer entertainment or gossip questions irrelevant to {{subject}}.
    5. Always respond in English.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])

    chain = prompt | llm | StrOutputParser()
    
    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )
    
    return chain_with_history

# --- 7. 处理用户输入 ---
# 输入框提示语改为英文
user_input = st.chat_input("Type your question here...")

if user_input:
    # 7.1 显示用户输入
    st.chat_message("human").write(user_input)
    
    # 7.2 获取处理链
    chain = get_chain(subject, style, temperature)
    
    # 7.3 流式输出 (Streaming) - 用户体验核心升级
    with st.chat_message("assistant"):
        # 使用 st.write_stream 配合 chain.stream 实现打字机效果
        # config 中传入 session_id 以匹配历史记录
        response = st.write_stream(
            chain.stream(
                {"input": user_input, "subject": subject},
                config={"configurable": {"session_id": "current_session"}}
            )
        )
    
    # 注意：使用 st.write_stream 后，Streamlit 不会自动把 AI 的完整回复存入 memory 对象吗？
    # 答案是：RunnableWithMessageHistory 会在 stream 结束时自动保存。
    # 但为了保险起见和立即更新状态，有时需要手动刷新或依赖下一次 rerun。
    # 在这里，LangChain 的 RunnableWithMessageHistory 会自动处理好后端存储。