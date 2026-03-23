import logging
import os
from app.core.config import settings
import replicate
import requests
logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self):
        logger.info("☁️ Đang khởi tạo TTSService (Replicate API)...")
        # Replicate tự động tìm biến REPLICATE_API_TOKEN trong hệ thống
        if not os.environ.get("REPLICATE_API_TOKEN"):
            logger.warning("⚠️ CHÚ Ý: Chưa tìm thấy REPLICATE_API_TOKEN trong môi trường!")
        logger.info("✅ TTS Sẵn sàng!")

    async def generate_speech(self ,  gen_text: str | None = None, ref_text: str | None = None, ref_audio_path: str | None = None) -> bytes:
        """
        Đẩy file mẫu và text lên Replicate, chờ GPU Cloud chạy rồi tải file audio về.
        
        Args:
            gen_text: Văn bản cần chuyển thành giọng nói
            ref_text: Văn bản tham chiếu
            ref_audio_path: Đường dẫn đến file audio tham chiếu
        """
        logger.info(f"Đang gửi yêu cầu F5-TTS lên Replicate cho câu: '{gen_text[:30]}...'")
        try:
            # Gọi API của Replicate (Sử dụng model F5-TTS phổ biến nhất trên đó)
            # Quá trình này tự động upload file ref_audio của bạn lên Cloud ẩn
            with open(ref_audio_path, "rb") as audio_file:
                output_url = replicate.run(
                    "x-lance/f5-tts:87faf6dd7a692dd82043f662e76369cab126a2cf1937e25a9d41e0b834fd230e",
                    input={
                        "gen_text": gen_text,
                        "ref_text": ref_text,
                        "ref_audio": audio_file,
                        "remove_silence": True
                    }
                )
            
            # Khác với OpenAI trả về Bytes, Replicate trả về 1 đường link URL chứa file Audio
            logger.info(f"✅ Replicate đã render xong. Đang tải âm thanh về...")
            
            # Tải file âm thanh từ link URL đó về máy
            response = requests.get(output_url)
            response.raise_for_status() # Kiểm tra xem tải có lỗi không
            
            # Trả về bytes trực tiếp cho Pipeline (Không cần lưu file)
            logger.info(f"✅ Đã nhận file TTS dạng Bytes từ Replicate.")
            return response.content
            
        except Exception as e:
            logger.error(f"❌ Lỗi khi gọi Replicate API: {str(e)}")
            raise e
# Khởi tạo instance
tts_service = TTSService()