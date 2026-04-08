import logging
from app.core.config import settings
from openai import OpenAI
from app.utils.tracking_model_llm import get_client
logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        print("🧠 Đang khởi tạo LLM Service...")
        self.client = get_client()

    def generate_response(self, user_text: str, chat_history: list , language: str) -> tuple[str, list]:
        """
        Nhận câu hỏi và lịch sử cũ. Trả về câu trả lời và lịch sử mới.
        """
        # Nếu lịch sử trống, nhét System Prompt vào đầu tiên
        if not chat_history:
            chat_history.append({"role": "system", "content": settings.llm_system_prompt + f"trả lời theo ngôn ngữ này {language}"})
            
        # Thêm câu của User vào
        chat_history.append({"role": "user", "content": user_text})

        # Gọi OpenAI API
        response = self.client.chat.completions.create(
            model=settings.llm_model,
            messages=chat_history,
            temperature=settings.llm_temperature
        )
        
        ai_text = response.choices[0].message.content
        
        # Lưu câu trả lời của AI vào lịch sử
        chat_history.append({"role": "assistant", "content": ai_text})
        
        return ai_text, chat_history

# Khởi tạo instance
llm_service = LLMService()