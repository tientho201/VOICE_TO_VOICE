import os

import requests
import streamlit as st
import uuid
import base64

st.set_page_config(page_title="Chatbot", page_icon=":robot:", layout="wide")

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# CSS Tùy chỉnh để làm đẹp Sidebar giống ChatGPT
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 2em;
    }
    .st-emotion-cache-11v6ept{
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Khởi tạo state
if "chat_counter" not in st.session_state:
    st.session_state.chat_counter = 1 # Bắt đầu đếm từ 1

# Khởi tạo state
if "chats" not in st.session_state:
    first_id = str(uuid.uuid4())
    st.session_state.chats = {
        first_id: {
            "name": "New Chat",
            "messages": [],
            "voice": None,
            "chat_number": st.session_state.chat_counter,
        }
    }
    st.session_state.active_session = first_id
    st.session_state.chat_selector = first_id
with st.sidebar:
    st.markdown("""
    <style>
        .st-emotion-cache-595tnf {
            display: none
        }
        .stElementContainer{
            margin: 0px
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRsuVEyccK0aMsEtY6SIeOCAs9GS_NRT8q0yQ&s", width="stretch")
    st.divider()
   
    st.title("📂 Danh sách Chat")
    
    if st.button("➕ Cuộc trò chuyện mới"):
        st.session_state.chat_counter += 1
        new_id = str(uuid.uuid4())
        st.session_state.chats[new_id] = {
            "name": "New Chat",
            "messages": [],
            "voice": None,
            "chat_number": st.session_state.chat_counter,
        }
        st.session_state.active_session = new_id
        st.rerun()  # Load lại trang
        
    st.divider()
    
    # 1. Lấy danh sách options hiện tại
    chat_options = list(st.session_state.chats.keys())

    # 2. Hàm format
    def format_func(option):
        return st.session_state.chats[option]["name"] + " (" + str(st.session_state.chats[option]["chat_number"]) + ")"

    # 3. Tính toán vị trí index hiện tại an toàn
    if st.session_state.active_session in chat_options:
        active_index = chat_options.index(st.session_state.active_session)
    else:
        active_index = 0
        st.session_state.active_session = chat_options[0]

    # 4. RADIO BỊ TƯỚC QUYỀN KEY - CHỈ CHẠY THEO INDEX
    selected_id = st.radio(
        "Chat history",
        options=chat_options,
        format_func=format_func,
        index=active_index  # Điều khiển trực tiếp bằng vị trí
    )

    # 5. Lắng nghe thay đổi từ User
    if selected_id != st.session_state.active_session:
        st.session_state.active_session = selected_id
        st.rerun()

    # 6. THUẬT TOÁN XÓA CỦA BẠN (Đã fix lỗi sai mục tiêu)
    if len(st.session_state.chats) > 1:
        if st.button("🗑️ Delete this chat"):
            # BƯỚC QUAN TRỌNG: Lấy mục tiêu xóa trực tiếp từ biến của Radio
            target_id = selected_id 
            current_index = chat_options.index(target_id)
            
            # Thực hiện xóa đúng mục tiêu đó
            del st.session_state.chats[target_id]
            
            # Lấy list key MỚI sau khi xóa
            new_keys = list(st.session_state.chats.keys())
            
            # Tính index gần nhất theo đúng logic của bạn
            nearest_index = min(current_index, len(new_keys) - 1)
            
            # Gán session vào index mới và load lại
            st.session_state.active_session = new_keys[nearest_index]
            st.rerun()

    st.divider()

    # Cấu hình API Key (Dùng chung cho tất cả)
    api_key = st.text_input("API Key", type="password")
    
    if api_key:
        st.success("API Key đã được cấu hình")
    else:
        st.error("Vui lòng cấu hình API Key")
    
col1, col2 = st.columns([2, 1], gap="xlarge")

with col2:
    if st.button("Health check"):
        try:
            r = requests.get(f"{BACKEND_URL}/health", timeout=10)
            st.success(r.json())
        except Exception as e:
            st.error(str(e))
    # 1. Khởi tạo bộ nhớ tạm thời cho Chat (Dùng xong tắt trình duyệt là mất)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    # 2. Hiển thị lịch sử trò chuyện
    st.divider()
    st.subheader("💬 Cuộc trò chuyện")
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["text"])
            if msg.get("audio"):
                st.audio(msg["audio"])

with col1:
    st.subheader("Upload hoặc Record audio")

    uploaded = st.file_uploader("Upload audio", type=["wav", "mp3", "m4a", "ogg", "flac"])
    recorded = st.audio_input("Record audio", sample_rate=48000)

    audio_file = recorded or uploaded

    if audio_file is not None:
        st.audio(audio_file)

        if st.button("Send Voice" , use_container_width=True):
            # Thêm tin nhắn của User vào lịch sử hiển thị ngay lập tức
            st.session_state.chat_history.append({
                "role": "user", 
                "text": "🎤 *Bạn vừa gửi một tin nhắn thoại...*", 
                "audio": audio_file.getvalue()
            })
            
            files = {
                "file": (
                    getattr(audio_file, "name", "recorded.wav"),
                    audio_file.getvalue(),
                    getattr(audio_file, "type", "audio/wav"),
                )
            }
            # Vừa hiện hiệu ứng xoay xoay vừa gọi API
            with st.spinner("Thinking..."):
                try:
                    r = requests.post(f"{BACKEND_URL}/v1/v2v", files=files, timeout=60)
                    r.raise_for_status()
                    response_data = r.json()
                    
                    # --- PHẦN QUAN TRỌNG: Bóc tách dữ liệu từ Backend ---
                    # Giả định backend của bạn trả về JSON có dạng: 
                    # {"text": "Câu trả lời của AI", "audio_base64": "UklGRiQAAABXQVZFZm10IBAA..."}
                    
                    ai_text = response_data.get("text", "AI không có câu trả lời bằng chữ.")
                    ai_audio_b64 = response_data.get("audio_base64", "")
                    
                    # Giải mã Base64 thành byte âm thanh để Streamlit đọc được
                    ai_audio_bytes = base64.b64decode(ai_audio_b64) if ai_audio_b64 else None
                    
                    # Lưu câu trả lời của AI vào bộ nhớ
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "text": ai_text,
                        "audio": ai_audio_bytes
                    })
                    
                    # Rerun để load lại giao diện và phát âm thanh mới nhất
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Lỗi kết nối hoặc xử lý: {str(e)}")
