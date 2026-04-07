import os 
from dotenv import load_dotenv , find_dotenv
from langsmith.wrappers import wrap_openai 
from openai import OpenAI
_ = load_dotenv(find_dotenv())

# Để dùng LangSmith, bạn đăng ký tài khoản tại https://smith.langchain.com/
# Sau đó tạo API Key và thay thế vào chuỗi trống bên dưới:
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY") # DÁN API KEY CỦA BẠN VÀO ĐÂY
os.environ["LANGCHAIN_PROJECT"] = "LIVE_CHAT_VOICE_CLONING" # Đã đổi tên để không bị nhầm lẫn với frontend

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = wrap_openai(openai_client)

def get_client():
    return client