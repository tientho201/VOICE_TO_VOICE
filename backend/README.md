# Voice-to-Voice Backend

Đây là dịch vụ backend cho dự án Voice-to-Voice, được xây dựng bằng [FastAPI](https://fastapi.tiangolo.com/). Dịch vụ này xử lý âm thanh và kết nối với các mô hình AI khác nhau để cung cấp các tính năng STT (Chuyển giọng nói thành văn bản), LLM (Mô hình ngôn ngữ lớn), và TTS (Chuyển văn bản thành giọng nói).

## Kiến trúc

Backend cung cấp một REST API để tiếp nhận các file âm thanh và xử lý chúng thông qua một pipeline:
1. **STT (Speech-to-Text):** Xử lý qua Groq (`whisper-large-v3-turbo`).
2. **LLM (Large Language Model):** Xử lý bởi OpenAI (`gpt-4o-mini`) nhằm tạo ra các câu trả lời tự nhiên dưới dạng đàm thoại.
3. **TTS (Text-to-Speech):** Xử lý bởi ElevenLabs với chất lượng cao, trả về giọng nói được clone tốc độ cực nhanh.

## Cấu trúc thư mục
- `app/api/`: API Routers (Endpoint `/v2v` xử lý tải file lên).
- `app/core/`: Thiết lập cấu hình cho các cấu hình API và biến môi trường thông qua `pydantic-settings`.
- `app/services/`: Tích hợp các dịch vụ cụ thể (`Groq`, `OpenAI`, `ElevenLabs`, và `v2v_pipeline`).

## Yêu cầu thiết yếu
- Python 3.9+
- Cung cấp các cấu hình API xác thực vào file `.env` theo biến:
  - `GROQ_API_KEY`
  - `OPENAI_API_KEY`
  - `ELEVENLABS_API_KEY`

## Cài đặt & Khởi chạy

1. **Cài đặt các thư viện phụ thuộc:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Chạy server:**
   Khởi động server phát triển FastAPI:
   ```bash
   fastapi dev app/main.py
   ```
   *Server sẽ chạy tại địa chỉ http://127.0.0.1:8000.*
