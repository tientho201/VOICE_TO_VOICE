from __future__ import annotations

from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Response
from pydantic import BaseModel
import base64
import logging
import os
import uuid
import urllib.parse
import json
from app.core.config import settings
from app.services.v2v_pipeline import v2v_pipeline
from app.services.stt import stt_service
from app.services.tts import tts_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter()

# Khai báo model phản hồi để đảm bảo định dạng nhất quán với Frontend (Ví dụ React/Vue)
class V2VResponse(BaseModel):
    success: bool
    user_text: str          # Văn bản mà Hệ thống STT nhận lại từ giọng nói Người dùng
    bot_text: str           # Văn bản Câu trả lời của Bộ não LLM
    bot_audio: bytes        # Audio file đã được encode base64
    error: str

@router.get("/health")
async def health_check():
    return {"status": "ok"}

async def handle_ref_audio(
    session_id : str | None = None, 
    audio_data: bytes | None = None,
    ref_text: str | None = None,
    ext: str | None = None
) -> tuple[str | None, str | None]:
    """
    Xử lý file reference audio nếu có.
    Trả về: final_ref_path, temp_ref_text_path
    """
    if ref_text is None:
        ref_text = ""
    temp_ref_audio_path = None
    temp_ref_text_path = None
    try:
        temp_dir = settings.temp_audio_dir
        os.makedirs(temp_dir, exist_ok=True)

        temp_ref_audio_path = os.path.join(temp_dir, f"ref_{session_id}.{ext}")
        temp_ref_text_path = os.path.join(temp_dir, f"ref_{session_id}.txt")
        with open(temp_ref_audio_path, "wb") as f:
            f.write(audio_data)
        with open(temp_ref_text_path, "w", encoding="utf-8") as f:
            f.write(ref_text)
        logger.info(f"Đã lưu temporary file reference audio tại {temp_ref_audio_path}")
        logger.info(f"Đã lưu temporary file reference text tại {temp_ref_text_path}")
    except Exception as e:
        logger.error(f"Lỗi extract file ref_audio_file: {str(e)}")
       
    return temp_ref_audio_path, temp_ref_text_path

@router.post("/chat", response_model=V2VResponse)
async def chat(
    audio_file: UploadFile = File(...),
    ref_audio_path: str | None = Form(None),
    ref_text_path: str | None = Form(None),
    chat_history: str | None = Form(None),
    language: str | None = Form(None),
    user_text: str | None = Form(None)
):
    """
    Endpoint chính của đồ án:
    - Nhận vào file audio (`wav`, `mp3`, `webm`) qua Multipart Form Data.
    - Tuỳ chọn nhận ref_audio_path hoặc ref_text_path để làm mẫu Voice Cloning cho TTS.
    - Truyền vào Pipeline: STT -> LLM -> TTS.
    - Trả về JSON chứa Text kết quả của người dùng, của bot & Audio Base64.
    """
    logger.info(f"Received audio file: {audio_file.filename}, type: {audio_file.content_type}")
    
    # 1. Đọc bytes file âm thanh
    audio_data = await audio_file.read()
    if not audio_data or len(audio_data) == 0:
        return{
            "success": False,
            "error": "Audio file is empty."
        }
    # 2. SỬA MÌN 1: Đọc nội dung file text một cách an toàn
    ref_text_content = ""
    if ref_text_path and os.path.exists(ref_text_path):
        with open(ref_text_path, "r", encoding="utf-8") as f:
            ref_text_content = f.read()
    # 3. SỬA MÌN 2: Bung chuỗi JSON thành list[dict]
    history_list = []
    if chat_history:
        try:
            history_list = json.loads(chat_history)
        except json.JSONDecodeError:
            logger.warning("Không thể parse chat_history, bắt đầu với lịch sử trống.")
            history_list = []
    try:
        # 3. Xử lý toàn bộ logic pipeline
        result = await v2v_pipeline.process_audio(
            audio_bytes=audio_data,
            ref_audio_path=ref_audio_path,
            ref_text=ref_text_content,
            chat_history=history_list,
            audio_filename=audio_file.filename,
            language=language,
            pre_transcribed_text=user_text
        )
        
        if not result.get("success"):
            return {
                "success": False,
                "error": result.get("error"),
                "user_audio": "",
                "user_text": "",
                "bot_text": "",
                "bot_audio": ""
            }
        audio_base64 = base64.b64encode(result["bot_audio_bytes"]).decode("utf-8")
        return V2VResponse(
            success=True,
            user_audio = base64.b64encode(audio_data).decode("utf-8"),
            user_text=result["user_text"],
            bot_text=result["bot_text"],
            bot_audio=audio_base64,
            error=""
        )
    except Exception as e:
        logger.error(f"Lỗi xử lý pipeline: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "user_audio": "",
            "user_text": "",
            "bot_text": "",
            "bot_audio": ""
        }

@router.post("/setup_voice")
async def setup_voice(
    audio_file: UploadFile = File(...),
    session_id : str | None = Form(None),
    ref_text: str | None = Form(None),
    language: str | None = Form(None)
):
    """
    Người dùng sẽ gửi file audio để setup giọng nói của mình
    Nhận vào sẽ là file audio và text tương ứng với file audio đó
    Trả về đường dẫn audio với tên là cùng session_id của đoạn chat
    
    Args:
        audio_file: File audio của người dùng
        session_id: ID của đoạn chat
        ref_text: Text tương ứng với file audio
    
    Returns:
        dict: Dictionary chứa đường dẫn audio
    """
    logger.info(f"Received audio file for streaming: {audio_file.filename}, type: {audio_file.content_type}")
    
    audio_data = await audio_file.read()
    if ref_text is None:
        logger.info(f" Bắt đầu xử lý STT...")
        ref_text = await stt_service.transcribe(audio_bytes=audio_data, audio_filename=audio_file.filename , language=language)
        logger.info(f" Kết quả STT: {ref_text}")
    if not audio_data or len(audio_data) == 0:
        return{
            "success": False,
            "error": "Audio file is empty."
        }
    original_filename = audio_file.filename or "audio.wav"
    ext = original_filename.split(".")[-1] # Lấy đuôi file
    ref_audio_path, ref_text_path = await handle_ref_audio(session_id, audio_data, ref_text, ext)
    # 2. Upload lên ElevenLabs lấy Voice ID
    voice_id = await tts_service.clone_voice(session_id=str(session_id), file_path=ref_audio_path)
    return {
        "success": True,
        "ref_audio_path": voice_id,
        "ref_text_path": ref_text_path,
        "ref_text": ref_text,
        "error": None
    }

@router.post("/stt_user")
async def stt_user(
    audio_file: UploadFile = File(...),
    language: str | None = Form(None)
):
    """
    Người dùng sẽ gửi file audio để chuyển từ audio sang text
    Trả về text tương ứng với file audio
    Args:
        audio_file: File audio của người dùng
    Returns:
        dict: Dictionary chứa text tương ứng với file audio
    """
    logger.info(f"Received audio file for streaming: {audio_file.filename}, type: {audio_file.content_type}")
    
    audio_data = await audio_file.read()
    logger.info(f" Bắt đầu xử lý STT...")
    ref_text = await stt_service.transcribe(audio_bytes=audio_data, audio_filename=audio_file.filename , language=language)
    logger.info(f" Kết quả STT: {ref_text}")
    if not audio_data or len(audio_data) == 0:
        return{
            "success": False,
            "error": "Audio file is empty."
        }
        
    return {
        "success": True,
        "user_text": ref_text,
        "error": None
    }

