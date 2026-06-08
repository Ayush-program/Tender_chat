from fastapi import APIRouter, HTTPException, Depends
from app.schemas import ChatRequest, ChatResponse
from app.ai_service import get_ai_response
from app.database import get_db
import aiosqlite

router = APIRouter(tags=["Chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: aiosqlite.Connection = Depends(get_db)):
    if not request.messages:
        raise HTTPException(status_code=400, detail="Messages cannot be empty")

    # Convert Pydantic models to dicts for AI service
    messages = [{"role": m.role, "content": m.content} for m in request.messages]

    try:
        reply = await get_ai_response(messages, lead_id=request.lead_id)
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        print(f"AI Error: {e}")
        error_text = str(e)
        if "model_decommissioned" in error_text:
            raise HTTPException(
                status_code=503,
                detail="Configured GROQ model is decommissioned. Set GROQ_MODEL to a supported model like llama-3.1-8b-instant.",
            )
        raise HTTPException(status_code=500, detail=f"AI service error: {error_text}")

    # Log to DB
    if request.lead_id:
        user_msg = messages[-1]["content"]
        await db.execute(
            "INSERT INTO chat_logs (lead_id, role, message) VALUES (?, ?, ?)",
            (request.lead_id, "user", user_msg)
        )
        await db.execute(
            "INSERT INTO chat_logs (lead_id, role, message) VALUES (?, ?, ?)",
            (request.lead_id, "assistant", reply)
        )
        await db.commit()

    return ChatResponse(reply=reply)
