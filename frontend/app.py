import os

import requests
import streamlit as st
import uuid
import base64

from src.lib import tracking_model


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
    /* Khóa cuộn cho thẻ html và body 
    /*html, body {    */
    /*    overflow: hidden !important;    */
    /*}*/
    
    /* Khóa cuộn cho container chính của Streamlit */
    /*[data-testid="stAppViewContainer"], */
    /*[data-testid="stMainBlockContainer"] {*/
    /*    overflow: hidden !important;*/
    /*}*/
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
            "chat_history": [],
            "ref_audio_bytes": None,
            "chat_number": st.session_state.chat_counter,
            "ref_text": tracking_model.create_text_random_voice(),
            "is_voice_cloned": False,
            "mic_key": str(uuid.uuid4()),
            "is_send_voice": False
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
    
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRsuVEyccK0aMsEtY6SIeOCAs9GS_NRT8q0yQ&s", width="content")
    st.divider()
   
    st.title("📂 List Chat")
    
    if st.button("➕ New Chat"):
        st.session_state.chat_counter += 1
        new_id = str(uuid.uuid4())
        st.session_state.chats[new_id] = {
            "name": "New Chat",
            "chat_history": [],
            "ref_audio_bytes": None,
            "chat_number": st.session_state.chat_counter,
            "ref_text": tracking_model.create_text_random_voice(),
            "is_voice_cloned": False,
            "mic_key": str(uuid.uuid4()),
            "is_send_voice": False
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

col1, col2 = st.columns([1, 1], gap="xlarge")

#===============================================
#                       COL1
#===============================================

with col1:
    st.subheader("Upload or Record audio")

    # KỊCH BẢN A: ĐÃ CLONE XONG -> Chỉ hiện file audio đã lưu và nút Reset
    if st.session_state.chats[st.session_state.active_session]["is_voice_cloned"] and "ref_audio_bytes" in st.session_state.chats[st.session_state.active_session]:
        st.success("✅ Voice cloned successfully!")
        
        # Phát lại âm thanh từ bộ nhớ Session State (Không bao giờ bị mất khi rerun)
        st.audio(st.session_state.chats[st.session_state.active_session]["ref_audio_bytes"])
        with st.status("Hãy nói theo nội dung bên dưới để clone giọng nói của bạn"):
            st.write(st.session_state.chats[st.session_state.active_session]["ref_text"])
        # Nút để người dùng thu âm lại từ đầu nếu muốn đổi giọng
        if st.button("🔄 Change voice", use_container_width=True):
            st.session_state.chats[st.session_state.active_session]["is_voice_cloned"] = False
            del st.session_state.chats[st.session_state.active_session]["ref_audio_bytes"]
            del st.session_state.chats[st.session_state.active_session]["ref_text"]
            st.session_state.chats[st.session_state.active_session]["ref_text"] = tracking_model.create_text_random_voice()
            st.rerun()

    else:

        uploaded = st.file_uploader("Upload audio", type=["wav", "mp3", "m4a", "ogg", "flac"])
        recorded = st.audio_input("Record audio", sample_rate=48000)
        audio_file = recorded or uploaded

        with st.status("Hãy nói theo nội dung bên dưới để clone giọng nói của bạn"):
            st.write(st.session_state.chats[st.session_state.active_session]["ref_text"])
        if audio_file is not None:
            # st.audio(audio_file)
            if st.button("Send Voice" , use_container_width=True):
                st.session_state.chats[st.session_state.active_session]["ref_audio_bytes"] = audio_file.getvalue()
                
                # Thành công -> Mở khóa mic bên cột 2
                st.session_state.chats[st.session_state.active_session]["is_voice_cloned"] = True
                st.success("Voice cloned successfully! You can start chatting in the next column.")
                st.rerun() # Load lại trang để mic bên col2 hết bị mờ



with col2:
    
    st.subheader("🎙️ Live Talk")

    # 1. TẠO KHUNG CHAT CỐ ĐỊNH (Cuộn được, đẩy mic xuống dưới)
    # Chỉnh height cho phù hợp với màn hình của bạn
    chat_container = st.container(height=500)
    
    # Vẽ lịch sử chat vào trong khung
    with chat_container:
        if not st.session_state.chats[st.session_state.active_session]["chat_history"]:
            st.info("Start the conversation by recording your voice!")
        for i, msg in enumerate(st.session_state.chats[st.session_state.active_session]["chat_history"]):
            with st.chat_message(msg["role"]):
                st.markdown(msg["text"])
                if msg.get("audio"):
                    # Chỉ tự động phát (autoplay) âm thanh CỦA AI và MỚI NHẤT
                    is_last_msg = (i == len(st.session_state.chats[st.session_state.active_session]["chat_history"]) - 1)
                    should_autoplay = is_last_msg and msg["role"] == "assistant"
                    
                    st.audio(msg["audio"], autoplay=should_autoplay)
    
    st.divider()
    
    # Cảnh báo cho người dùng biết tại sao mic bị mờ
    if not st.session_state.chats[st.session_state.active_session]["is_voice_cloned"]:
        st.warning("⚠️ Please complete the Voice Cloning step in the left column to start the conversation.")
    
    # 2. KHỞI TẠO KEY ĐỘNG CHO MIC
    # Streamlit có một nhược điểm: khi ghi âm xong, file audio sẽ nằm kẹt ở widget đó.
    # Ta phải dùng một key thay đổi liên tục để "ép" cái mic reset lại sau mỗi lần gửi.
    if "mic_key" not in st.session_state:
        st.session_state.mic_key = str(uuid.uuid4())
    
    # Mic ghi âm giờ đã bị đẩy xuống dưới cùng
    recorded_speech = st.audio_input(
        "Press to speak", 
        sample_rate=48000, 
        key=st.session_state.mic_key,
        disabled= not st.session_state.chats[st.session_state.active_session]["is_voice_cloned"]
    )
    
    # 3. VÒNG LẶP XỬ LÝ LIVE (Khi có người dùng nói)
    if recorded_speech and st.session_state.chats[st.session_state.active_session]["is_voice_cloned"]:
        audio_bytes = recorded_speech.getvalue()
        # A. Lưu lời của bạn vào lịch sử
        # st.session_state.chat_history.append({
        #     "role": "user",
        #     "text": "🎤 *You just sent a voice message...*",
        #     "audio": audio_bytes
        # })
        # B. Ép Streamlit vẽ ngay lời của bạn và hiệu ứng "AI đang suy nghĩ" ra màn hình 
        # (Không chờ gọi API xong mới vẽ, như vậy mới ra chất Live)
        with chat_container:
            with st.chat_message("user"):
                st.markdown("🎤 *You just sent a voice message...*")
                st.audio(audio_bytes)
            
            with st.chat_message("assistant"):
                with st.spinner("AI is listening and thinking..."):
                    
                    # --- GỌI BACKEND V2V CỦA BẠN Ở ĐÂY ---
                    # Gửi file thu âm Live
                    files = {
                        "file": ("recorded.wav", audio_bytes, "audio/wav"),
                        "ref_text" : st.session_state.ref_text,
                       
                    }
                    
                    # QUAN TRỌNG: Phải gửi kèm file mẫu giọng bên cột Setup để Server Clone đúng chuẩn
                    if "ref_audio_bytes" in st.session_state.chats[st.session_state.active_session]:
                        files["ref_audio_file"] = ("ref_audio.wav", st.session_state.chats[st.session_state.active_session]["ref_audio_bytes"], "audio/wav")
                    
                    try:
                        # Phải gọi `/v2v` thay vì `/v2v/stream` vì đoạn code dưới của bạn đang parse đuôi `.json()` 
                        # (chứ API stream trả về file bytes thô)
                        r = requests.post(f"{BACKEND_URL}/v2v", files=files, timeout=60)
                        r.raise_for_status()
                        res = r.json()
                        
                        # Bóc tách dữ liệu JSON (Cập nhật đúng biến bot_text từ Server gửi về)
                        ai_text = res.get("bot_text", "AI has processed the audio.")
                        ai_audio_b64 = res.get("bot_audio_base64", "")
                        ai_audio_bytes = base64.b64decode(ai_audio_b64) if ai_audio_b64 else None
                        
                        # C. Lưu lời của AI vào lịch sử
                        st.session_state.chats[st.session_state.active_session]["chat_history"].append({
                            "role": "assistant",
                            "text": ai_text,
                            "audio": ai_audio_bytes
                        })
                        
                        # D. BƯỚC QUYẾT ĐỊNH: Đổi key để dọn dẹp cái Mic, sẵn sàng cho câu tiếp theo
                        st.session_state.chats[st.session_state.active_session]["mic_key"] = str(uuid.uuid4())
                        
                        # Load lại toàn bộ trang để kích hoạt Autoplay âm thanh của AI
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Backend connection error: {str(e)}")
                        # Nếu lỗi cũng phải reset mic để thu âm lại
                        st.session_state.chats[st.session_state.active_session]["mic_key"] = str(uuid.uuid4())
                        if st.button("Refresh"):
                            st.rerun()
