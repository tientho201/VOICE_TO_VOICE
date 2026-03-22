# Voice-to-Voice Frontend

Đây là giao diện người dùng frontend cho dự án Voice-to-Voice, được xây dựng bằng [Streamlit](https://streamlit.io/). Giao diện này cung cấp trải nghiệm đàm thoại thân thiện nhằm tương tác với trợ lý AI qua giọng nói kèm theo khả năng tự động phát lại âm thanh.

## Các tính năng chính

- **Thiết lập sao chép giọng nói (Voice Cloning Setup):** Tải lên hoặc trực tiếp thu âm một mẫu giọng nói của bạn. Hệ thống sẽ lưu lại an toàn để sử dụng sao chép giống y hệt chất giọng của bạn cho các phản hồi kế tiếp.
- **Giao diện Chat:** Giao diện trò chuyện tương tác bao gồm lịch sử tin nhắn của người dùng, văn bản và các file phản hồi âm thanh từ hệ thống AI.
- **Đàm thoại trực tiếp (Live Talk):** Nói tương tác qua microphone và ngay lập tức nhận lại phản hồi bằng giọng nói từ trợ lý AI với tính năng tự động phát giọng âm cực mượt.
- **Theo dõi cùng LangSmith:** Tích hợp sẵn mã giám sát, tra soát hệ thống bằng LangChain telemetry.

## Yêu cầu thiết yếu
- Python 3.9+

## Cài đặt & Khởi chạy

1. **Cài đặt các thư viện phụ thuộc:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Biến môi trường:**
   Tạo hoặc cấu hình một file `.env` với các nội dung thiết lập sau:
   ```env
   BACKEND_URL=http://127.0.0.1:8000
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=your_langsmith_key
   LANGCHAIN_PROJECT=RANDOM_TEXT_VOICE_CLONING
   OPENAI_API_KEY=your_openai_key
   ```

3. **Chạy ứng dụng:**
   ```bash
   streamlit run app.py
   ```
   *Giao diện UI sẽ tự động mở tại http://localhost:8501.*
