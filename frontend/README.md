# Voice-to-Voice Frontend

This is the frontend user interface for the Voice-to-Voice project, built with [Streamlit](https://streamlit.io/). It provides a user-friendly conversational interface to interact with the AI assistant through voice and audio playback.

## Features

- **Voice Cloning Setup:** Upload or record an audio sample of your voice. The system will securely save it to clone your voice for responses.
- **Chat Interface:** An interactive chat UI containing user messages and AI text/audio responses.
- **Live Talk:** Speak into your microphone and immediately get a spoken response back from the AI with an auto-playing audio feature.
- **LangSmith Tracing:** Includes scripts for tracing and system monitoring utilizing LangChain telemetry.

## Prerequisites
- Python 3.9+

## Setup & Running

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables:**
   A `.env` config file with the following variables is necessary:
   ```env
   BACKEND_URL=http://127.0.0.1:8000
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=your_langsmith_key
   LANGCHAIN_PROJECT=RANDOM_TEXT_VOICE_CLONING
   OPENAI_API_KEY=your_openai_key
   ```

3. **Run the Application:**
   ```bash
   streamlit run app.py
   ```
   *The UI will launch automatically at http://localhost:8501.*
