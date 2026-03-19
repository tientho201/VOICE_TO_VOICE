from __future__ import annotations

from fastapi import APIRouter, File, UploadFile

router = APIRouter()


@router.get("/health")
def health():
    return {"ok": True}


@router.post("/v1/v2v")
async def voice_to_voice(file: UploadFile = File(...)):
    """
    Placeholder endpoint:
    - Nhận audio (wav/mp3/...) từ frontend
    - Sau này bạn nối pipeline: STT -> LLM -> TTS
    """
    data = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "bytes_received": len(data),
        "message": "Received. Hook your STT->LLM->TTS pipeline here.",
    }

