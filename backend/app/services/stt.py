import logging
from app.core.config import settings
from groq import Groq
import os
logger = logging.getLogger(__name__)

class STTService:
    def __init__(self):
        logger.info("🎧 Đang khởi tạo STT Service (Groq API)...")
        if not os.environ.get("GROQ_API_KEY"):
            logger.warning("⚠️ CHÚ Ý: Chưa tìm thấy GROQ_API_KEY trong môi trường!")
        self.client = Groq(api_key=settings.groq_api_key)
        logger.info("✅ Groq STT Sẵn sàng!")
    async def transcribe(self, audio_bytes: str , language: str = "vi" , audio_filename: str = "") -> str:
        """
        Nhận luồng bytes từ Frontend, ném thẳng lên Groq mà không cần lưu file
        """
        try:
            logger.info(f"Đang xử lý STT cho audio bytes")
            file_upload = (audio_filename, audio_bytes)
            response = self.client.audio.transcriptions.create(
                model=settings.model,
                file=file_upload,
                response_format="text", # Lấy thẳng chuỗi text cho lẹ, không cần JSON rườm rà
                temperature=settings.temperature  # Optional
            )
            logger.info(f"STT Response: {response}")
            return response
        
        except Exception as e:
            logger.error(f"Lỗi STT: {e}")
            return ""

stt_service = STTService()
