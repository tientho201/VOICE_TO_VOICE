# Voice-to-Voice LLM Chatbot Monorepo

Welcome to the **Voice-to-Voice** Project! This monorepo contains the complete source code for a real-time conversational AI system supporting voice cloning, Speech-to-Text (STT), Large Language Models (LLM), and Text-to-Speech (TTS).

The architecture is split into a **Backend** (FastAPI) handling all the AI processing, and a **Frontend** (Streamlit) providing a seamless, chat-centric voice interface.

## 🚀 Key Features
- 🎙️ **Real-time Voice Recording:** Interactive UI allowing users to record their voice from the browser.
- 🗣️ **Live Voice Cloning:** Read a dynamically generated script to provide a sample audio, which is then used to clone your voice for the AI's responses!
- ⚡ **High-Performance Pipeline:**
  - **STT**: Instant transcription using **Groq** (whisper-large-v3-turbo).
  - **LLM**: Core intelligence provided by **OpenAI** (gpt-4o-mini).
  - **TTS**: Fast and premium voice cloning generation via **Replicate** (F5-TTS).
- 💬 **Live Audio Autoplay**: Fully integrated stream playback in an intuitive ChatGPT-like format.

## 📁 Repository Structure

- **`backend/`**: FastAPI Server. Holds the `v2v_pipeline` which chains STT, LLM, and TTS together. Exposes endpoints (`/v2v`) for processing multipart audio file uploads. 
- **`frontend/`**: Streamlit Web UI. Manages chat history logs, microphone functionality, dynamic layouts, configures user profiles, and interfaces requests to the backend.
- **`temp_data/`**: Folders auto-generated locally on runtime, used by the API to process intermediate `.wav` transactions securely.

## ⚙️ Quick Start

### 1. Requirements

Ensure you have Python 3.9+ installed natively or within virtual environments.
Generate the following API access keys:
- [Groq](https://console.groq.com) for fast STT.
- [OpenAI](https://platform.openai.com) for LLM & Frontend prompts.
- [Replicate](https://replicate.com) to access the F5-TTS model endpoint.

**Configure `.env`**: Make a `.env` in the root (which both frontend and backend will load):
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

### 2. Run the Backend

Launch a terminal session, navigate to the `backend` folder, and run:
```bash
cd backend
pip install -r requirements.txt
fastapi dev app/main.py
```
*Backend operates at `http://127.0.0.1:8000`*

### 3. Run the Frontend

Open another terminal session, navigate to the `frontend` folder, and run:
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```
*The URL will pop up automatically indicating your frontend is live (typically `http://localhost:8501`).*
