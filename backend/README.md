## Backend (Voice-to-Voice)

Nơi đặt API + pipeline xử lý Voice-to-Voice (STT → LLM → TTS) và/hoặc streaming audio realtime.

### Thư mục

- `app/api/`: endpoint REST/WebSocket
- `app/services/`: `stt`, `tts`, `llm`, `audio_io`, `streaming`
- `app/core/`: config/settings

### Chạy backend

Tại thư mục `backend/`:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
fastapi run .\backend\app\main.py
```

Test nhanh:

- `GET /health`
- `POST /v1/v2v` (form-data key `file`)
