<div align="center">

# 🎙️ Voice-to-Voice AI Chatbot

**Trợ lý đàm thoại AI theo thời gian thực với Voice Cloning**

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

> Hệ thống AI cho phép bạn **nói chuyện tự nhiên** với một trợ lý thông minh — và nhận lại câu trả lời bằng chính **giọng nói được clone từ giọng của bạn**.

</div>

---

## 📌 Mục lục

- [Tổng quan](#-tổng-quan)
- [Tính năng nổi bật](#-tính-năng-nổi-bật)
- [Kiến trúc hệ thống](#-kiến-trúc-hệ-thống)
- [Cấu trúc thư mục](#-cấu-trúc-thư-mục)
- [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
- [Cài đặt & Khởi chạy](#-cài-đặt--khởi-chạy)
  - [Phương thức 1: Chạy thủ công (Local)](#phương-thức-1-chạy-thủ-công-local)
  - [Phương thức 2: Docker Compose](#phương-thức-2-docker-compose)
- [Biến môi trường](#-biến-môi-trường)
- [API Reference](#-api-reference)
- [Công nghệ sử dụng](#-công-nghệ-sử-dụng)

---

## 🧠 Tổng quan

**Voice-to-Voice AI Chatbot** là một ứng dụng AI đàm thoại thời gian thực được xây dựng theo kiến trúc microservice, bao gồm:

- **Backend** (FastAPI): Xử lý toàn bộ pipeline AI gồm STT → LLM → TTS.
- **Frontend** (Streamlit): Giao diện web tương tác, cho phép ghi âm trực tiếp từ trình duyệt.

Điểm độc đáo của hệ thống là khả năng **clone giọng nói người dùng** và sử dụng giọng đó để phát lại câu trả lời của AI, tạo ra trải nghiệm giao tiếp hoàn toàn cá nhân hoá.

---

## ✨ Tính năng nổi bật

| Tính năng                    | Mô tả                                                                          |
| ---------------------------- | ------------------------------------------------------------------------------ |
| 🎙️ **Ghi âm thời gian thực** | Giao diện cho phép ghi âm trực tiếp ngay từ trình duyệt web                    |
| 🧬 **Voice Cloning**         | Phân tích và sao chép phong cách giọng nói của người dùng từ một đoạn mẫu ngắn |
| ⚡ **STT tốc độ cao**        | Chuyển giọng nói → văn bản với **Groq Whisper** (whisper-large-v3-turbo)       |
| 🤖 **LLM thông minh**        | Tạo câu trả lời thông minh thông qua **OpenAI GPT-4o-mini**                    |
| 🔊 **TTS & Voice Cloning**   | Tổng hợp giọng nói tự nhiên bằng **ElevenLabs**, clone từ giọng người dùng     |
| 💬 **Auto-play phản hồi**    | Tự động phát audio phản hồi ngay sau khi AI xử lý xong                         |
| 🐳 **Docker Support**        | Hỗ trợ triển khai đầy đủ với Docker Compose                                    |

---

## 🏗️ Kiến trúc hệ thống

```
┌─────────────────────────────────────────────────────────────┐
│                        NGƯỜI DÙNG                           │
│                   (Trình duyệt web)                         │
└──────────────────────────┬──────────────────────────────────┘
                           │  Ghi âm / Phát audio
                           ▼
┌─────────────────────────────────────────────────────────────┐
│               FRONTEND  (Streamlit :8501)                   │
│  • Quản lý microphone & lịch sử chat                        │
│  • Hiển thị UI tương tác                                    │
│  • Gửi audio file → Backend API                             │
└──────────────────────────┬──────────────────────────────────┘
                           │  HTTP POST /v2v
                           ▼
┌─────────────────────────────────────────────────────────────┐
│               BACKEND  (FastAPI :8000)                      │
│                                                             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐                 │
│  │   STT    │──▶│   LLM    │──▶│   TTS    │                │
│  │  Groq    │   │  OpenAI  │   │ElevenLabs│                 │
│  │ Whisper  │   │GPT-4o-m  │   │  Clone   │                 │
│  └──────────┘   └──────────┘   └──────────┘                 │
│              v2v_pipeline.py                                │
└─────────────────────────────────────────────────────────────┘
```

**Pipeline xử lý một request:**

1. Frontend gửi file audio (WAV) lên Backend
2. **STT** (Groq Whisper): Chuyển audio → text
3. **LLM** (GPT-4o-mini): Sinh câu trả lời từ text
4. **TTS** (ElevenLabs): Tổng hợp audio từ câu trả lời, dùng giọng đã clone
5. Backend trả về file audio → Frontend tự động phát

---

## 📁 Cấu trúc thư mục

```text
CODE/
├── README.md                    # Tài liệu dự án (file này)
├── docker-compose.yml           # Cấu hình Docker Compose
├── .env                         # Biến môi trường (không commit!)
├── .gitignore
│
├── backend/                     # FastAPI Server
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py              # Entry point & lifespan management
│       ├── api/
│       │   └── routes.py        # API endpoints (/v2v, ...)
│       ├── core/
│       │   └── config.py        # Pydantic settings
│       ├── services/
│       │   ├── stt.py           # Speech-to-Text (Groq Whisper)
│       │   ├── llm.py           # Language Model (OpenAI)
│       │   ├── tts.py           # Text-to-Speech (ElevenLabs)
│       │   └── v2v_pipeline.py  # Pipeline chính nối 3 service
│       ├── models/              # Pydantic request/response models
│       └── utils/               # Tiện ích (file handling, ...)
│
├── frontend/                    # Streamlit Web App
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py                   # Entry point giao diện
│   ├── public/                  # Static assets
│   └── src/
│       ├── components/          # UI components
│       ├── pages/               # Các trang giao diện
│       └── lib/
│           └── tracking_model.py
│
├── shared/                      # Code dùng chung (nếu có)
├── temp_data/                   # Thư mục chứa file audio tạm thời
└── docs/                        # Tài liệu bổ sung
```

---

## 🔧 Yêu cầu hệ thống

- **Python** 3.9 hoặc cao hơn
- **Docker & Docker Compose** (nếu chạy bằng container)
- API Keys từ các dịch vụ bên thứ ba:

| Dịch vụ                    | Mục đích                 | Đăng ký                                            |
| -------------------------- | ------------------------ | -------------------------------------------------- |
| **Groq**                   | Speech-to-Text (Whisper) | [console.groq.com](https://console.groq.com)       |
| **OpenAI**                 | LLM (GPT-4o-mini)        | [platform.openai.com](https://platform.openai.com) |
| **ElevenLabs**             | TTS & Voice Cloning      | [elevenlabs.io](https://elevenlabs.io)             |
| **LangSmith** _(tuỳ chọn)_ | Tracing & monitoring     | [smith.langchain.com](https://smith.langchain.com) |

---

## 🚀 Cài đặt & Khởi chạy

### Bước 0: Clone dự án & cấu hình `.env`

```bash
git clone https://github.com/tientho201/VOICE_TO_VOICE.git
cd VOICE_TO_VOICE
```

Tạo file `.env` tại thư mục gốc dựa trên mẫu sau:

```env
# ======================
# AI Service API Keys
# ======================
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# ======================
# Frontend Configuration
# ======================
BACKEND_URL=http://127.0.0.1:8000

# ======================
# LangSmith Tracing (tuỳ chọn)
# ======================
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=VOICE_TO_VOICE
```

> ⚠️ **Lưu ý bảo mật**: File `.env` đã được thêm vào `.gitignore`. Tuyệt đối **không commit** file này lên Git.

---

### Phương thức 1: Chạy thủ công (Local)

#### 1.1 Khởi chạy Backend

```bash
cd backend
pip install -r requirements.txt
fastapi dev app/main.py
```

Backend sẽ chạy tại: **`http://127.0.0.1:8000`**  
Swagger UI: **`http://127.0.0.1:8000/docs`**

#### 1.2 Khởi chạy Frontend

Mở terminal mới tại thư mục gốc:

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

Giao diện web sẽ mở tự động tại: **`http://localhost:8501`**

---

### Phương thức 2: Docker Compose

Cách nhanh nhất để khởi chạy toàn bộ hệ thống:

```bash
# Build và khởi chạy tất cả service
docker compose up --build

# Chạy ở chế độ nền (detached)
docker compose up --build -d

# Dừng tất cả service
docker compose down
```

| Service              | URL                          |
| -------------------- | ---------------------------- |
| Frontend (Streamlit) | `http://localhost:8501`      |
| Backend (FastAPI)    | `http://localhost:8000`      |
| API Docs (Swagger)   | `http://localhost:8000/docs` |

---

## 🌐 Biến môi trường

| Biến                   | Bắt buộc | Mô tả                        |
| ---------------------- | -------- | ---------------------------- |
| `GROQ_API_KEY`         | ✅       | API key của Groq (STT)       |
| `OPENAI_API_KEY`       | ✅       | API key của OpenAI (LLM)     |
| `ELEVENLABS_API_KEY`   | ✅       | API key của ElevenLabs (TTS) |
| `BACKEND_URL`          | ✅       | URL của Backend API          |
| `LANGCHAIN_TRACING_V2` | ❌       | Bật/tắt LangSmith tracing    |
| `LANGCHAIN_API_KEY`    | ❌       | API key LangSmith            |
| `LANGCHAIN_PROJECT`    | ❌       | Tên project trên LangSmith   |

---

## 📡 API Reference

Sau khi Backend khởi chạy, truy cập **`http://localhost:8000/docs`** để xem đầy đủ Swagger UI.

| Method | Endpoint  | Mô tả                               |
| ------ | --------- | ----------------------------------- |
| `POST` | `/v2v`    | Xử lý pipeline Voice-to-Voice chính |
| `GET`  | `/health` | Health check endpoint               |

---

## 🛠️ Công nghệ sử dụng

| Lớp                    | Công nghệ                               | Phiên bản |
| ---------------------- | --------------------------------------- | --------- |
| **Backend Framework**  | FastAPI                                 | latest    |
| **Frontend Framework** | Streamlit                               | 1.x       |
| **STT Model**          | Groq Whisper (`whisper-large-v3-turbo`) | —         |
| **LLM**                | OpenAI GPT-4o-mini                      | —         |
| **TTS & Cloning**      | ElevenLabs                              | —         |
| **Validation**         | Pydantic v2                             | 2.x       |
| **Config Management**  | pydantic-settings                       | 2.x       |
| **Containerization**   | Docker & Docker Compose                 | —         |
| **Monitoring**         | LangSmith (tuỳ chọn)                    | —         |

---

<div align="center">

Made with ❤️ by **tientho201**

</div>
