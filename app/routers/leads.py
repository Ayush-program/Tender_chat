from fastapi import APIRouter, HTTPException, Depends
from app.schemas import LeadCreate, LeadResponse
from app.database import get_db
import aiosqlite

router = APIRouter(tags=["Leads"])

@router.post("/lead", response_model=LeadResponse)
async def create_lead(lead: LeadCreate, db: aiosqlite.Connection = Depends(get_db)):
    # Check for duplicate email
    async with db.execute(
        "SELECT id FROM leads WHERE email = ?", (lead.email,)
    ) as cursor:
        existing = await cursor.fetchone()

    if existing:
        # Return existing lead (user refreshed page)
        return LeadResponse(success=True, lead_id=existing[0], name=lead.name)

    async with db.execute(
        "INSERT INTO leads (name, email, mobile) VALUES (?, ?, ?)",
        (lead.name, lead.email, lead.mobile)
    ) as cursor:
        lead_id = cursor.lastrowid

    await db.commit()
    print(f"✅ New Lead: {lead.name} | {lead.email} | {lead.mobile}")
    return LeadResponse(success=True, lead_id=lead_id, name=lead.name)
