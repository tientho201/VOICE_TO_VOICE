# Voice-to-Voice Backend

This is the backend service for the Voice-to-Voice project, built with [FastAPI](https://fastapi.tiangolo.com/). It handles audio processing and connects to various AI models to provide STT, LLM, and TTS capabilities.

## Architecture

The backend exposes a REST API to accept audio files and handles the processing via a pipeline:
1. **STT (Speech-to-Text):** Processed via Groq (`whisper-large-v3-turbo`).
2. **LLM (Large Language Model):** Powered by OpenAI (`gpt-4o-mini`) to generate conversational responses.
3. **TTS (Text-to-Speech):** F5-TTS via Replicate API for high fidelity and fast voice cloning generation.

## Project Structure
- `app/api/`: API Routers (`/v2v` endpoint handling file uploads).
- `app/core/`: Configuration settings for API Keys and variables via `pydantic-settings`.
- `app/services/`: Integration of specific services (`Groq`, `OpenAI`, `Replicate`, and `v2v_pipeline`).

## Prerequisites
- Python 3.9+
- Provide the following exact API variables in an `.env` file mapping:
  - `GROQ_API_KEY`
  - `OPENAI_API_KEY`
  - `REPLICATE_API_TOKEN`

## Setup & Running

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server:**
   Start the FastAPI development server:
   ```bash
   fastapi dev app/main.py
   ```
   *The server runs on http://127.0.0.1:8000.*
