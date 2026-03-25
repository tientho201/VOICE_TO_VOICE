import logging
import os
import asyncio
import uuid
import tempfile
from app.services.stt import stt_service
from app.services.llm import llm_service
from app.services.tts import tts_service
from app.core.config import settings
logger = logging.getLogger(__name__)


class V2VPipeline:
    async def process_audio(self, audio_bytes: bytes, ref_audio_path: str = None, ref_text: str = None, chat_history: list = None, audio_filename: str = "") -> dict:
        """
        Thực thi luồng V2V an toàn với Concurrency.
        Nếu ref_audio_path và ref_text được truyền vào (từ bước Setup UI), sẽ dùng nó để clone.
        Nếu không có, fallback về việc tự lấy file live làm mẫu.
        """
        temp_output_path = os.path.join(tempfile.gettempdir(), f"output_{uuid.uuid4()}.wav")
        try:

            # BƯỚC 1: STT
            logger.info(f" Bắt đầu xử lý STT...")
            user_text = await stt_service.transcribe(audio_bytes=audio_bytes, audio_filename=audio_filename)
            logger.info(f" Kết quả STT: {user_text}")

            if not user_text:
                raise ValueError("Không nhận diện được giọng nói.")

            # BƯỚC 2: LLM (Lưu ý: Sau này cần truyền thêm history vào đây)
            logger.info(f" Bắt đầu xử lý LLM...")
            bot_text , chat_history = llm_service.generate_response(user_text , chat_history)
            logger.info(f" Kết quả LLM: {bot_text}")

            # BƯỚC 3: TTS
            logger.info("Bắt đầu xử lý TTS với ElevenLabs...")
            
            # Cái biến ref_audio_path lúc này chứa chuỗi ID (ví dụ: "pNInz6obbfdqIeY...")
            bot_audio_bytes = await tts_service.generate_speech(
                gen_text=bot_text,
                voice_id=ref_audio_path 
            )

            return {
                "success": True,
                "user_text": user_text,
                "bot_text": bot_text,
                "bot_audio_bytes": bot_audio_bytes
            }
            
        except Exception as e:
            logger.error(f"Lỗi V2V Pipeline: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            pass

v2v_pipeline = V2VPipeline()