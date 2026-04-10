import os 
from dotenv import load_dotenv , find_dotenv
from langsmith.wrappers import wrap_openai 
from openai import OpenAI
_ = load_dotenv(find_dotenv())

# Để dùng LangSmith, bạn đăng ký tài khoản tại https://smith.langchain.com/
# Sau đó tạo API Key và thay thế vào chuỗi trống bên dưới:
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY") # DÁN API KEY CỦA BẠN VÀO ĐÂY
os.environ["LANGCHAIN_PROJECT"] = "RANDOM_TEXT_VOICE_CLONING" # Tên dự án sẽ hiện trên dashboard

openai_client = OpenAI()
client = wrap_openai(openai_client)

def create_text_random_voice():
    text = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Bạn là một trợ lý AI. Tạo cho tôi một đoạn văn thực hiện dự án voice cloning"},
            {"role": "user", "content": "Tạo cho tôi đoạn văn ngắn gọn khoảng 20 đến 30 từ với ước tính thời gian để tôi voice cloning khoảng 10 giây. Chỉ đưa ra đoạn text thôi không đưa ra gì thêm. Giọng văn phải tự nhiên, không máy móc và đoạn văn đó không phải là mời mở đầu có thể là một đoạn văn ngẫu nhiên nào đó khiến cho người dùng khi nhìn vào là muốn đọc. "}
        ]
    )
    return text.choices[0].message.content