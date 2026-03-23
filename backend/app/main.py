from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from app.api.routes import router as api_router
from contextlib import asynccontextmanager
import shutil
from app.core.config import settings

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # ==========================================
    # KHÚC NÀY CHẠY KHI BẬT SERVER (STARTUP)
    # ==========================================
    print(f"🧹 Đang khởi động Server... Dọn dẹp thư mục {settings.temp_audio_dir}")
    
    # Kiểm tra xem thư mục có tồn tại không
    if os.path.exists(settings.temp_audio_dir):
        # Cách nhanh nhất: Xóa trắng nguyên cái thư mục đó cùng mọi thứ bên trong
        shutil.rmtree(settings.temp_audio_dir)
        print("✅ Đã xóa sạch file audio cũ.")
    
    # Tạo lại một thư mục mới tinh, trống rỗng để sẵn sàng hứng file mới
    os.makedirs(settings.temp_audio_dir, exist_ok=True)
    print("✅ Thư mục temp/data đã sẵn sàng!")
    
    yield # Bàn giao lại quyền điều khiển cho FastAPI chạy ứng dụng
    
    # ==========================================
    # KHÚC NÀY CHẠY KHI TẮT SERVER (SHUTDOWN)
    # ==========================================
    print("🛑 Đang tắt Server... Tạm biệt!")
    # (Bạn có thể thêm code dọn dẹp lúc tắt server ở đây nếu muốn)
def create_app() -> FastAPI:
    app = FastAPI(title="Voice-to-Voice Backend", version="0.1.0", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)
    return app


app = create_app()

