import os
import asyncio
import logging
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings

logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self):
        logger.info("☁️ Đang khởi tạo TTSService (ElevenLabs)...")
        api_key = os.environ.get("ELEVENLABS_API_KEY")
        if not api_key:
            logger.warning("⚠️ Chưa tìm thấy ELEVENLABS_API_KEY trong file .env!")
        
        # Khởi tạo Client của ElevenLabs
        self.client = ElevenLabs(api_key=api_key)
        logger.info("✅ ElevenLabs TTS Sẵn sàng!")

    async def clone_voice(self, session_id: str, file_path: str) -> str:
        """Upload file âm thanh lên ElevenLabs để tạo Voice ID"""
        logger.info(f"Đang upload file mẫu lên ElevenLabs để clone giọng...")
        
        def _add_voice():
            try:
                # Đặt tên cho cái giọng vừa clone (để dễ quản lý trên web ElevenLabs)
                voice_name = f"Clone_User_{session_id}"
                
                # Gọi API tạo giọng
                with open(file_path, "rb") as f:
                    voice = self.client.voices.ivc.create(
                        name=voice_name,
                        files=[f]
                    )
                logger.info(f"✅ Clone thành công! Voice ID: {voice.voice_id}")
                return voice.voice_id
            except Exception as e:
                logger.error(f"❌ Lỗi khi clone giọng ElevenLabs: {str(e)}")
                raise e
                
        # Chạy bất đồng bộ
        voice_id = await asyncio.to_thread(_add_voice)
        return voice_id

    async def generate_speech(self, gen_text: str, voice_id: str) -> bytes:
        """Tạo âm thanh từ Text sử dụng Voice ID đã clone"""
        if not voice_id:
            raise ValueError("Không tìm thấy Voice ID! Vui lòng Clone giọng trước.")
            
        logger.info(f"Đang gọi ElevenLabs TTS cho câu: '{gen_text[:30]}...'")
        
        def _generate():
            try:
                # GỌI ĐÚNG CÚ PHÁP TỪ DOCS MỚI NHẤT CỦA ELEVENLABS
                audio_generator = self.client.text_to_speech.convert(
                    voice_id=voice_id,
                    output_format="mp3_44100_128", # Chuẩn MP3 nhẹ, chất lượng cao
                    text=gen_text,
                    model_id="eleven_flash_v2_5", # Model đọc Tiếng Việt cực đỉnh
                )
                
                # ElevenLabs trả về dữ liệu dạng chunk, ta nối nó lại thành 1 cục bytes
                audio_bytes = b"".join(list(audio_generator))
                logger.info("✅ ElevenLabs đã render xong! Tốc độ chớp nhoáng.")
                return audio_bytes
            except Exception as e:
                logger.error(f"❌ Lỗi OpenAI TTS API: {str(e)}")
                raise e

        # Chạy bất đồng bộ
        bot_audio_bytes = await asyncio.to_thread(_generate)
        return bot_audio_bytes

# Khởi tạo instance
tts_service = TTSService()

