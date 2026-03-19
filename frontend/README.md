## Frontend (Voice-to-Voice)

Web UI cho Voice-to-Voice:

- Record hoặc upload audio
- Hiển thị chat (nếu có)
- Nhận audio trả về và phát realtime

### Chạy frontend (Streamlit)

Tại thư mục `frontend/`:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
set BACKEND_URL=http://127.0.0.1:8000
streamlit run app.py
```

