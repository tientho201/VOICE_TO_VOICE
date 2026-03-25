import os
from pydantic_settings import BaseSettings, SettingsConfigDict

from dotenv import load_dotenv , find_dotenv
_ = load_dotenv(find_dotenv())

class Settings(BaseSettings):
    app_name: str = "Voice-to-Voice Backend"
    
    # ==========================================
    # 1. CẤU HÌNH STT (Faster-Whisper - Chạy Local)
    # ==========================================
    model: str = "whisper-large-v3-turbo"      # Các size: base, small, medium, large-v3
    temperature: float = 0.5
    groq_api_key: str = os.getenv("GROQ_API_KEY")
    # ==========================================
    # 2. CẤU HÌNH LLM (OpenAI API - Chạy Cloud)
    # ==========================================
    llm_model: str = "gpt-4o-mini"
    # System prompt được tối ưu cực gắt cho TTS: Bỏ hẳn markdown và emoji
    llm_system_prompt: str = """Bạn là một trợ lý ảo giao tiếp bằng GIỌNG NÓI. 
QUY TẮC SINH TỒN (BẮT BUỘC TUÂN THỦ):
1. Trả lời như đang nói chuyện trực tiếp, siêu ngắn gọn, đi thẳng vào trọng tâm. TỐI ĐA 3-4 CÂU.
2. TUYỆT ĐỐI KHÔNG sử dụng Markdown. KHÔNG dùng ký tự đặc biệt (*, #, -, _). KHÔNG in đậm, KHÔNG in nghiêng, KHÔNG xuống dòng tạo danh sách.
3. Chỉ sử dụng chữ cái, số, và các dấu câu cơ bản (chấm, phẩy, hỏi chấm, chấm than).
4. Viết mọi thứ thành một đoạn văn duy nhất để hệ thống chuyển đổi giọng nói (TTS) đọc trôi chảy."""
    llm_temperature: float = 0.7
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    
    # ==========================================
    # 3. CẤU HÌNH TTS (F5-TTS - Chạy Local)
    # ==========================================
    tts_device: str = "cpu"
    # Khai báo sẵn các tham số an toàn cho F5-TTS
    tts_target_rms: float = 0.1        # Chuẩn hóa âm lượng đầu ra
    tts_cross_fade_duration: float = 0.15 # Độ mượt khi nối các câu dài
    
    # ==========================================
    # 4. CẤU HÌNH HỆ THỐNG (Lưu trữ)
    # ==========================================
    # Thay vì dùng thư mục temp mặc định của hệ điều hành, ta gom gọn vào project
    temp_audio_dir: str = "./temp_data"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

settings = Settings()

# Tự động tạo thư mục temp nếu nó chưa tồn tại lúc khởi động app
os.makedirs(settings.temp_audio_dir, exist_ok=True)