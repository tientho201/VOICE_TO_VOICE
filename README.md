## Voice-to-Voice Monorepo

Cấu trúc đề xuất cho đề tài **Voice-to-Voice** gồm `backend/` (API + xử lý audio) và `frontend/` (UI web).

### Cấu trúc thư mục

- **`backend/`**: Server/API và pipeline Voice-to-Voice (STT/LLM/TTS), websocket/streaming (nếu cần)
  - `app/api/`: route/controller (REST/WebSocket)
  - `app/core/`: config, settings, logging
  - `app/services/`: nghiệp vụ (stt, tts, llm, audio streaming)
  - `app/models/`: schema/DTO
  - `app/utils/`: tiện ích (audio, file, time, ...)
  - `tests/`: test
- **`frontend/`**: Web UI (upload/record, realtime playback, chat)
  - `src/components/`: UI components
  - `src/pages/`: pages/screens
  - `src/lib/`: api client, helpers
  - `public/`: static assets
- **`shared/`**: tài nguyên dùng chung (contract, sample audio, ...)
- **`docs/`**: tài liệu (proposal, architecture, api spec)

### Gợi ý tiếp theo

- Mình sẽ dựng sẵn **backend FastAPI** (REST + WebSocket streaming audio) và **frontend (Streamlit)**, kèm ví dụ luồng: record → gửi chunk → nhận audio trả về → phát realtime.
