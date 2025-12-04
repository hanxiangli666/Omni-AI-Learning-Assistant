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
st.set_page_config(page_title="全能AI学习助手", page_icon="🎓")
st.title("🎓 全能 AI 学习助手")

# --- 3. 状态管理 (Session State) ---
if "chat_store" not in st.session_state:
    st.session_state["chat_store"] = ChatMessageHistory()
    # 初始欢迎语
    st.session_state["chat_store"].add_ai_message("你好！我是你的全能学习助手。请选择学科开始提问吧！")

# 辅助函数：获取历史记录
def get_session_history(session_id: str):
    return st.session_state["chat_store"]

# --- 4. 侧边栏设置 (功能升级区) ---
with st.sidebar:
    st.header("⚙️ 设置")
    
    # 4.1 学科扩展：新增 生物、物理
    subject = st.selectbox(
        "📚 选择学科", 
        options=["计算机", "数学", "物理", "生物", "文学", "历史"]
    )
    
    # 4.2 风格选择
    style = st.selectbox(
        "🗣️ 讲解风格", 
        options=["简洁直接", "详细教学", "苏格拉底式引导"]
    )
    
    # 4.3 高级设置：创造力参数 (新增功能)
    with st.expander("🛠️ 模型参数 (高级)"):
        temperature = st.slider(
            "创造力 (Temperature)", 
            min_value=0.0, max_value=1.0, value=0.3, step=0.1,
            help="数值越高回答越随机发散，数值越低越严谨。理科建议调低，文科建议调高。"
        )
    
    # 4.4 清空对话按钮 (新增功能)
    if st.button("🗑️ 清空当前对话", use_container_width=True):
        st.session_state["chat_store"].clear()
        st.session_state["chat_store"].add_ai_message(f"已重置。现在我们开始聊聊关于 **{subject}** 的话题吧！")
        st.rerun()

# --- 5. 聊天界面渲染 ---
# 遍历历史记录并显示
for msg in st.session_state["chat_store"].messages:
    role = "assistant" if msg.type == "ai" else "human"
    # 针对代码和公式优化显示
    st.chat_message(role).write(msg.content)

# --- 6. 核心逻辑 (LCEL链) ---
def get_chain(subject, style, temperature):
    # 6.1 模型初始化 (动态传入 temperature)
    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="deepseek-chat", # 或 gpt-3.5-turbo
        base_url="https://api.deepseek.com",
        temperature=temperature,
        streaming=True # 开启流式支持
    )

    # 6.2 风格与提示词字典
    style_prompts = {
        "简洁直接": "直接给出核心答案，不要废话。如果是理科问题，直接列出公式和结果。",
        "详细教学": "像老师一样循循善诱。1. 先给出直接结论；2. 逐步拆解原理；3. 举一个生活中的例子来类比。",
        "苏格拉底式引导": "不要直接给答案。通过反问和提示，引导用户自己思考出答案。一步步引导。"
    }

    # 6.3 系统提示词 (针对物理/生物做了优化)
    # 特别增加了 LaTeX 格式说明，这对物理/数学很重要
    system_prompt = f"""你是 {{subject}} 领域的资深专家导师。
    
    请遵循以下讲解风格：
    {style_prompts[style]}
    
    注意事项：
    1. 如果涉及公式，请使用 LaTeX 格式（例如 $E=mc^2$）。
    2. 如果涉及生物/化学反应，请清晰列出反应式。
    3. 如果涉及代码，请使用代码块。
    4. 严厉拒绝回答与 {{subject}} 无关的娱乐八卦问题。
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])

    # 6.4 组装链
    chain = prompt | llm | StrOutputParser()
    
    # 6.5 挂载记忆
    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )
    
    return chain_with_history

# --- 7. 处理用户输入 ---
user_input = st.chat_input("输入你的问题...")

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