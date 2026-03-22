# Voice-to-Voice LLM Chatbot Monorepo

Chào mừng đến với dự án **Voice-to-Voice**! Kho lưu trữ này chứa đựng toàn bộ mã nguồn của hệ thống Trợ lý đàm thoại AI theo thời gian thực có hỗ trợ sao chép giọng nói (Voice Cloning), Speech-to-Text (STT), Mô hình ngôn ngữ lớn (LLM), và Text-to-Speech (TTS).

Kiến trúc phần mềm được phân chia rõ bao gồm một **Backend** (FastAPI) chuyên trách việc xử lý mọi tác vụ AI, và một **Frontend** (Streamlit) chuyên phục vụ giao diện trò chuyện bằng giọng nói mượt mà, thân thiện với người dùng.

## 🚀 Các tính năng nổi bật
- 🎙️ **Ghi âm trực tiếp theo thời gian thực:** Giao diện tương tác cho phép người dùng ghi âm trực tiếp ngay từ trình duyệt.
- 🗣️ **Sao chép giọng nói trực tiếp:** Yêu cầu người dùng đọc một đoạn văn bản được tạo ra ngẫu nhiên, sau đó lấy bản thu nhằm biến nó thành cơ sở nhân bản ra cùng phong cách chất giọng cho câu trả lời của AI!
- ⚡ **Quy trình xử lý âm thanh tốc độ cao:**
  - **STT**: Chuyển giọng nói sang văn bản tức thì sử dụng nền tảng của **Groq** (whisper-large-v3-turbo).
  - **LLM**: Não bộ tạo trả lời thông minh cung cấp bởi **OpenAI** (gpt-4o-mini) chuyên biệt để đối đáp đàm thoại.
  - **TTS**: Tạo lập file giọng âm đàm thoại mới được clone từ **Replicate** (F5-TTS).
- 💬 **Tự động phát giọng (Live Audio Autoplay)**: Tích hợp hoàn toàn các luồng phát lại trực tiếp tới format trình diễn trực quan mô phỏng giao tiếp tương tự ChatGPT.

## 📁 Cấu trúc lưu trữ

- **`backend/`**: FastAPI Server. Chứa `v2v_pipeline` nhằm xâu chuỗi logic các bước STT, LLM và TTS lại với nhau. Cung cấp API endpoint (`/v2v`) cho các thao tác tải lên và xử lý phân giải định dạng tệp tin âm thanh. 
- **`frontend/`**: Giao diện UI Web ứng dụng Streamlit. Có chức năng quản lý lịch sử trò chuyện, điều khiển các module microphone, tạo giao diện dàn bố cục linh động và giúp người sử dụng giao tiếp gián tiếp qua backend.
- **`temp_data/`**: Các thư mục sẽ tự động xuất hiện để giúp hỗ trợ các APIs trong việc giữ lại biên mục tạm thời các files `.wav` trung gian đảm bảo vòng đời request xử lý được chuẩn xác và an toàn.

## ⚙️ Hướng dẫn cài đặt nhanh

### 1. Yêu cầu hệ thống

Hãy đảm bảo máy chạy của bạn có thiết lập Python 3.9+ trở lên.
Nghiêm túc tạo trước và cung cấp các mã Token xác thực API Access Keys bảo mật từ các nền tảng:
- [Groq](https://console.groq.com) dành cho dịch vụ STT.
- [OpenAI](https://platform.openai.com) dành cho dịch vụ LLM trợ lý & tự động tạo text cho prompt Frontend.
- [Replicate](https://replicate.com) gọi lên service tạo giọng âm cho hệ tính F5-TTS.

**Cấu hình biến môi trường `.env`**: Hãy khai báo một file `.env` ở thư mục gốc căn nguyên của project (hầu hết backend và frontend sẽ trỏ file tại khu này):
```env
# AI Models Keys
GROQ_API_KEY=your_groq_key
OPENAI_API_KEY=your_openai_key
REPLICATE_API_TOKEN=your_replicate_token

# Frontend Configuration
BACKEND_URL=http://127.0.0.1:8000
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=RANDOM_TEXT_VOICE_CLONING
```

### 2. Khởi chạy Backend

Sau đó, truy cập bằng cửa sổ giao diện dòng lệnh terminal, đi vào folder `backend` và chạy trực tiếp cài đặt sau:
```bash
cd backend
pip install -r requirements.txt
fastapi dev app/main.py
```
*Backend sẽ đi vào hoạt động ở đường dẫn `http://127.0.0.1:8000`*

### 3. Khởi chạy Frontend

Vẫn trên góc độ thư mục gốc, gọi thêm dòng lệnh terminal command thứ 2, chọn vào thẳng directory `frontend`:
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```
*Trình duyệt web UI sẽ tự động khởi động bung lên báo hiệu Giao diện đã tương tác được qua địa chỉ `http://localhost:8501`.*
