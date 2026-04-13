import os

import requests
import streamlit as st
import uuid
import base64
import json
from src.lib import tracking_model


st.set_page_config(page_title="Chatbot", page_icon=":robot:", layout="wide" , initial_sidebar_state="collapsed")

BACKEND_URL = os.getenv("BACKEND_URL")

# CSS Tùy chỉnh để làm đẹp Sidebar giống ChatGPT
st.markdown("""
<style>
    /* 1. Màn hình PC lớn (24 inch trở lên, ngang > 1600px): Giữ nguyên 100% */
    @media screen and (min-width: 1600px) {
        html { zoom: 1.0; }
    }

    /* 2. Màn hình Laptop trung bình (14 - 16.5 inch): Ép thu nhỏ xuống 85% */
    @media screen and (max-width: 1599px) and (min-width: 1025px) {
        html { zoom: 0.85; }
    }

    /* 3. Màn hình nhỏ, Tablet, Mobile (Dưới 14 inch): Ép thu nhỏ xuống 75% */
    @media screen and (max-width: 1024px) {
        html { zoom: 0.75; }
    }
    
    /* Ép khung nội dung dàn đều, cắt bỏ khoảng trắng thừa ở 2 bên và trên dưới */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 98% !important; 
    }
    
    /* Thu gọn chiều cao của thanh phát âm thanh */
    audio {
        width: 100% !important;
        height: 45px !important;
    }
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
# label = r'''
#     $\textsf{
#     \Huge Text \huge Text \LARGE Text \Large Text 
#     \large Text \normalsize Text \small Text 
#     \footnotesize Text \scriptsize Text \tiny Text 
#     }$
# '''

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
            "ref_audio_path": None,
            "ref_text_path": None
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
            "ref_audio_path": None,
            "ref_text_path": None
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
    try:
        r_health = requests.get(f"{BACKEND_URL}/health")
        r_health.raise_for_status()
        res = r_health.json()
        if res["status"] == "ok":
            st.success("✅ Backend is running!")
    except Exception as e:
        st.error("❌ Backend is not running!")
        st.rerun()
    
col1, col2 = st.columns([1, 1], gap="xlarge")

#===============================================
#                       COL1
#===============================================

with col1:
    st.title("Upload or Record audio")

    # KỊCH BẢN A: ĐÃ CLONE XONG -> Chỉ hiện file audio đã lưu và nút Reset
    if st.session_state.chats[st.session_state.active_session]["is_voice_cloned"] and "ref_audio_bytes" in st.session_state.chats[st.session_state.active_session]:
        st.success("✅ Voice cloned successfully!")
        
        # Phát lại âm thanh từ bộ nhớ Session State (Không bao giờ bị mất khi rerun)
        st.audio(st.session_state.chats[st.session_state.active_session]["ref_audio_bytes"])
        with st.container(border=True):
            st.subheader("Nội dung để clone giọng nói" , divider="gray" )
            st.write(st.session_state.chats[st.session_state.active_session].get("ref_text", ""))
        # Nút để người dùng thu âm lại từ đầu nếu muốn đổi giọng
        if st.button("🔄 Change voice", use_container_width=True):
            st.session_state.chats[st.session_state.active_session]["is_voice_cloned"] = False
            st.session_state.chats[st.session_state.active_session].pop("ref_audio_bytes", None)
            st.session_state.chats[st.session_state.active_session].pop("ref_audio_path", None)
            st.session_state.chats[st.session_state.active_session].pop("ref_text_path", None)
            st.session_state.chats[st.session_state.active_session]["ref_text"] = tracking_model.create_text_random_voice()
            st.rerun()

    else:
        st.subheader("Upload audio")
        uploaded = st.file_uploader("Upload audio", type=["wav", "mp3", "m4a", "ogg", "flac"] , label_visibility= "collapsed")
        st.subheader("Record audio")
        recorded = st.audio_input("Record audio", sample_rate=48000 , label_visibility= "collapsed")
        audio_file = recorded or uploaded
        with st.container(border=True):
            st.subheader("Hãy nói theo nội dung bên dưới để clone giọng nói của bạn" , divider="gray" )
            st.write(st.session_state.chats[st.session_state.active_session].get("ref_text", ""))
        if audio_file is not None:
            if st.button("Send Voice" , use_container_width=True):
                st.session_state.chats[st.session_state.active_session]["ref_audio_bytes"] = audio_file.getvalue()
                files = {
                    "audio_file": (audio_file.name,   st.session_state.chats[st.session_state.active_session]["ref_audio_bytes"], audio_file.type),
                }
                    
                data = {
                    "session_id": st.session_state.chats[st.session_state.active_session]["mic_key"],
                    "ref_text": st.session_state.chats[st.session_state.active_session].get("ref_text") if recorded else None
                }
                    
                try:
                        
                    r = requests.post(f"{BACKEND_URL}/setup_voice", files=files, data=data, timeout=90)
                    r.raise_for_status()
                    res = r.json()
                        
                    if not res.get("success"):
                        if res.get("is_hallucination"):
                            st.warning(f"⚠️ {res.get('error')} Vui lòng thử upload/ghi âm diễn đạt rõ hơn.")
                            if "ref_audio_bytes" in st.session_state.chats[st.session_state.active_session]:
                                del st.session_state.chats[st.session_state.active_session]["ref_audio_bytes"]
                        else:
                            st.error(f"Thất bại: {res.get('error')}")
                    else:
                        st.session_state.chats[st.session_state.active_session]["is_voice_cloned"] = True
                        st.session_state.chats[st.session_state.active_session]["ref_audio_path"] = res.get("ref_audio_path")
                        st.session_state.chats[st.session_state.active_session]["ref_text_path"] = res.get("ref_text_path")
                        st.session_state.chats[st.session_state.active_session]["ref_text"] = res.get("ref_text")
                        # Thành công -> Mở khóa mic bên cột 2
                        st.success("Voice cloned successfully! You can start chatting in the next column.")
                        # Load lại toàn bộ trang để kích hoạt Autoplay âm thanh của AI
                        st.rerun()
                            
                except Exception as e:
                    st.error(f"Backend connection error: {str(e)}")
                    if st.button("Refresh"):
                        st.rerun()
                


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
    # Mic ghi âm giờ đã bị đẩy xuống dưới cùng
    recorded_speech = st.audio_input(
        "Press to speak", 
        sample_rate=48000, 
        key=st.session_state.chats[st.session_state.active_session]["mic_key"],
        disabled= not st.session_state.chats[st.session_state.active_session]["is_voice_cloned"]
    )
    
    # Lấy các biến ngắn gọn để dễ code
    current_chat = st.session_state.chats[st.session_state.active_session]

    # 3. VÒNG LẶP XỬ LÝ LIVE (Khi có người dùng nói)
    if recorded_speech and st.session_state.chats[st.session_state.active_session]["is_voice_cloned"]:
        audio_bytes = recorded_speech.getvalue()
        # B. Ép Streamlit vẽ ngay lời của bạn và hiệu ứng "AI đang suy nghĩ" ra màn hình 
        # (Không chờ gọi API xong mới vẽ, như vậy mới ra chất Live)
        # --- GỌI BACKEND V2V CỦA BẠN Ở ĐÂY ---
        # Gửi file thu âm Live
        files = {
            "audio_file": (recorded_speech.name, audio_bytes, recorded_speech.type),
        }
        
        # Cờ để kiểm tra STT có thành công không
        stt_success = False 
        user_text = ""
        
        with chat_container:
            with st.chat_message("user"):
                try:

                    r = requests.post(f"{BACKEND_URL}/stt_user", files=files, timeout=60)
                    r.raise_for_status()
                    res = r.json()
                    if not res.get("success"):
                        st.error(f"Thất bại: {res.get('error')}")
                    else:
                        user_text = res.get("user_text")
                        st.session_state.chats[st.session_state.active_session]["chat_history"].append({
                            "role": "user",
                            "text": user_text,
                            "audio": audio_bytes
                        })
                        st.markdown(f"🎤 {user_text}")
                        st.audio(audio_bytes)
                        stt_success = True
                except Exception as e:
                    st.error(f"Backend connection error: {str(e)}")
                    if st.button("Refresh"):
                        st.rerun()
            if stt_success:
                with st.chat_message("assistant"):
                    with st.spinner("AI is listening and thinking..."):
                        try:
                            clean_history = []
                            for msg in current_chat["chat_history"]:
                                # Cần đổi chữ "text" thành "content" để OpenAI hiểu
                                clean_history.append({"role": msg["role"], "content": msg["text"]})
                            data = {
                                "ref_audio_path": st.session_state.chats[st.session_state.active_session]["ref_audio_path"] ,
                                "ref_text_path": st.session_state.chats[st.session_state.active_session]["ref_text_path"],
                                "chat_history": json.dumps(clean_history)
                            }
                            r_chat = requests.post(f"{BACKEND_URL}/chat", files=files, data=data, timeout=20)
                            r_chat.raise_for_status()
                            res_chat = r_chat.json()
                            if not res_chat.get("success"):
                                st.error(f"Thất bại: {res_chat.get('error')}")
                            else:
                                ai_audio_bytes = base64.b64decode(res_chat.get("bot_audio")) if res_chat.get("bot_audio") else None
                                current_chat["chat_history"].append({
                                    "role": "assistant",
                                    "text": res_chat.get("bot_text"),
                                    "audio": ai_audio_bytes
                                })
                                # Đổi key và rerun CHỈ KHI MỌI THỨ THÀNH CÔNG
                                current_chat["mic_key"] = str(uuid.uuid4())
                                st.rerun()
                        except requests.exceptions.ReadTimeout:
                            st.error("Server xử lý quá lâu. Lỗi Timeout.")
                            if st.button("Refresh", key=f"ref_time_{current_chat['mic_key']}"): st.rerun()
                        except Exception as e:
                            st.error(f"Lỗi kết nối Chat: {str(e)}")
                            if st.button("Refresh", key=f"ref_chat_{current_chat['mic_key']}"): st.rerun()