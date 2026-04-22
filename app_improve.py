import streamlit as st
import time
from rag import RagService  # 确保 rag.py 在同级目录下

# ==========================================
# 1. 页面配置与初始化
# ==========================================
st.set_page_config(page_title="智能客服助手", page_icon="🤖", layout="wide")

# --- 模拟数据库 (实际项目请替换) ---
if 'user_db' not in st.session_state:
    st.session_state['user_db'] = {'admin': '123456', 'danny': '123'}

# --- 初始化会话状态 ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ""
    st.session_state['sessions'] = {}  # 存储所有对话 {id: [messages]}
    st.session_state['current_session'] = None

# --- 初始化 RAG 服务 ---
# 使用 cache_resource 确保模型只加载一次，不随页面刷新重置
@st.cache_resource
def get_rag_service():
    return RagService()

rag_service = get_rag_service()

# ==========================================
# 2. 登录与注册逻辑
# ==========================================
def login():
    st.title("🔒 系统登录")
    tab1, tab2 = st.tabs(["登录", "注册"])

    with tab1:
        username = st.text_input("用户名", key="login_user")
        password = st.text_input("密码", type="password", key="login_pwd")
        if st.button("登录"):
            if username in st.session_state['user_db'] and st.session_state['user_db'][username] == password:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.rerun()
            else:
                st.error("用户名或密码错误")

    with tab2:
        new_user = st.text_input("新用户名", key="reg_user")
        new_pwd = st.text_input("新密码", type="password", key="reg_pwd")
        if st.button("注册"):
            if new_user in st.session_state['user_db']:
                st.warning("用户已存在")
            else:
                st.session_state['user_db'][new_user] = new_pwd
                st.success("注册成功，请去登录")

def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = ""
    st.session_state['sessions'] = {}
    st.session_state['current_session'] = None
    st.rerun()

# ==========================================
# 3. 侧边栏：会话管理
# ==========================================
def sidebar_ui():
    with st.sidebar:
        st.write(f"👋 欢迎, **{st.session_state['username']}**")
        st.button("退出登录", on_click=logout, use_container_width=True)
        st.divider()

        # 新建对话按钮
        if st.button("➕ 新建对话", use_container_width=True):
            # 生成一个简单的唯一ID (实际项目可用 UUID)
            new_id = f"对话_{int(time.time())}"
            st.session_state['sessions'][new_id] = []
            st.session_state['current_session'] = new_id
            st.rerun()

        st.divider()
        st.markdown("### 📂 历史会话")

        # 遍历历史会话
        if not st.session_state['sessions']:
            st.info("暂无历史对话")

        # 为了让删除按钮和对话按钮对齐，我们遍历 ID
        for session_id in st.session_state['sessions']:
            # 使用列布局：左边是切换按钮，右边是删除按钮
            col1, col2 = st.columns([4, 1])

            with col1:
                # 切换会话按钮
                # 截取名字显示，避免太长
                display_name = session_id if len(session_id) < 10 else session_id[:8] + "..."
                if st.button(
                    f"💬 {display_name}",
                    key=f"btn_{session_id}",
                    use_container_width=True,
                    help="点击切换"
                ):
                    st.session_state['current_session'] = session_id
                    st.rerun()

            with col2:
                # 删除会话按钮 (使用红色样式)
                if st.button(
                    "❌",
                    key=f"del_{session_id}",
                    help="删除此对话"
                ):
                    # 1. 删除数据
                    del st.session_state['sessions'][session_id]
                    # 2. 如果当前正看着这个对话，重置当前会话
                    if st.session_state['current_session'] == session_id:
                        # 尝试切换到剩下的第一个对话，或者设为 None
                        remaining = list(st.session_state['sessions'].keys())
                        st.session_state['current_session'] = remaining[0] if remaining else None
                    st.rerun()

# ==========================================
# 4. 主界面：聊天逻辑
# ==========================================
def main_chat():
    # 确保有一个当前会话
    if not st.session_state['current_session']:
        # 如果有历史会话，自动切换到第一个
        if st.session_state['sessions']:
            first_key = list(st.session_state['sessions'].keys())[0]
            st.session_state['current_session'] = first_key
        else:
            # 如果没有，创建一个默认的
            new_id = f"对话_{int(time.time())}"
            st.session_state['sessions'][new_id] = []
            st.session_state['current_session'] = new_id

    st.title("💬 智能客服助手")
    st.caption(f"当前会话 ID: {st.session_state['current_session']}")

    # --- 显示历史消息 ---
    # 获取当前会话的消息列表
    messages = st.session_state['sessions'][st.session_state['current_session']]

    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- 处理用户输入 ---
    if prompt := st.chat_input("请输入您的问题..."):
        # 1. 添加用户消息到当前会话
        messages.append({"role": "user", "content": prompt})

        # 2. 显示用户消息
        with st.chat_message("user"):
            st.markdown(prompt)

        # 3. 调用 RAG 生成回复 (流式)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try:
                # 真正的 RAG 调用
                # 注意：这里使用的是 rag_service.chain (不是 base_chain)
                # config 用于传递 session_id 给 RunnableWithMessageHistory
                stream = rag_service.chain.stream(
                    {"input": prompt},
                    config={"configurable": {"session_id": st.session_state['current_session']}}
                )

                # 逐字显示
                for chunk in stream:
                    full_response += chunk + " "
                    message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)

                # 4. 将 AI 回复保存到当前会话
                messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                st.error(f"发生错误: {e}")
                messages.append({"role": "assistant", "content": "抱歉，系统发生错误。"})

# ==========================================
# 5. 程序入口
# ==========================================
def main():
    if st.session_state['logged_in']:
        sidebar_ui()
        main_chat()
    else:
        login()

if __name__ == "__main__":
    main()