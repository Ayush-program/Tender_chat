from fastapi import APIRouter, Depends
from app.database import get_db
from typing import List
import aiosqlite

router = APIRouter(tags=["Admin"])

@router.get("/leads")
async def get_all_leads(db: aiosqlite.Connection = Depends(get_db)):
    db.row_factory = aiosqlite.Row
    async with db.execute(
        "SELECT id, name, email, mobile, created_at FROM leads ORDER BY created_at DESC"
    ) as cursor:
        rows = await cursor.fetchall()
    return [dict(row) for row in rows]

@router.get("/stats")
async def get_stats(db: aiosqlite.Connection = Depends(get_db)):
    async with db.execute("SELECT COUNT(*) FROM leads") as c:
        total = (await c.fetchone())[0]
    async with db.execute(
        "SELECT COUNT(*) FROM leads WHERE DATE(created_at) = DATE('now')"
    ) as c:
        today = (await c.fetchone())[0]
    async with db.execute("SELECT COUNT(*) FROM chat_logs WHERE role='user'") as c:
        total_msgs = (await c.fetchone())[0]
    return {"total_leads": total, "today_leads": today, "total_messages": total_msgs}
