import logging
from app.core.config import settings
from groq import Groq
import os

logger = logging.getLogger(__name__)

_HALLUCINATION_TOKENS = [
    "ghiền mì gõ", "đăng ký kênh", "bấm vào đây", "xem thêm video",
    "chia sẻ video", "cảm ơn đã xem" , "subscribe", "like and subscribe", "thank you for watching", "thanks for watching",
    "please subscribe", "don't forget to", "hit the bell", "comment below", "amara.org",
]

class STTHallucinationError(Exception):
    pass

class STTService:
    def __init__(self):
        logger.info("🎧 Đang khởi tạo STT Service (Groq API)...")
        if not os.environ.get("GROQ_API_KEY"):
            logger.warning("⚠️ CHÚ Ý: Chưa tìm thấy GROQ_API_KEY trong môi trường!")
        self.client = Groq(api_key=settings.groq_api_key)
        logger.info("✅ Groq STT Sẵn sàng!")

    def _is_hallucination(self, text: str) -> bool:
        lower = text.lower().strip()
        if len(lower) < 3:
            return True
        for token in _HALLUCINATION_TOKENS:
            if token in lower:
                return True
        return False

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
                language=language,
                response_format="text", # Lấy thẳng chuỗi text cho lẹ, không cần JSON rườm rà
                temperature=settings.temperature  # Optional
            )
            logger.info(f"STT Response: {response}")
            
            if self._is_hallucination(response):
                raise STTHallucinationError("Âm thanh bị nhiễu hoặc không nhận diện được giọng nói. Vui lòng thu âm quá trình rõ ràng hơn!")
                
            return response
        
        except STTHallucinationError as e:
            raise e
        except Exception as e:
            logger.error(f"Lỗi STT: {e}")
            raise Exception("Lỗi nhận diện giọng nói hoặc âm thanh lỗi. Vui lòng thu âm lại!")

stt_service = STTService()
