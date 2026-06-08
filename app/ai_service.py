import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from typing import List, Dict

load_dotenv()

# ═══════════════════════════════════════════════════
# COMPANY KNOWLEDGE BASE — Edit this for your client
# ═══════════════════════════════════════════════════
SYSTEM_PROMPT = """You are a professional AI assistant for TenderPro Services — India's leading tender management and consultancy company.

COMPANY OVERVIEW:
TenderPro Services helps businesses win government and private tenders across India. With 10+ years of experience, we have assisted 500+ clients in winning tenders worth ₹2000+ crores.

OUR SERVICES:
1. Tender Identification — We find relevant tenders from GeM, CPPP, state portals that match your business.
2. Tender Documentation — Complete preparation of tender documents, technical & financial bids.
3. EMD & Bid Bond Assistance — Help with Earnest Money Deposit and bid security arrangements.
4. Eligibility Analysis — We review eligibility before applying to avoid disqualification.
5. Bid Strategy & Pricing — Competitive pricing strategy to maximize your win probability.
6. Tender Filing & Submission — End-to-end submission on your behalf (online & offline).
7. Post-Award Support — Contract review, performance guarantee, work order management.
8. Company Registration — MSME registration, GeM portal onboarding, ISO certification guidance.
9. Vendor Empanelment — Empanelment with PSUs, government departments, and large private firms.
10. Legal & Compliance — Tender-related legal documentation and compliance support.

SECTORS WE SERVE:
Construction & Infrastructure, IT & Software, Medical Equipment & Supplies, Electrical & Civil Works,
Manpower & Security Services, Printing & Stationery, Catering & Housekeeping, Consulting Services.

WHY CHOOSE TENDERPRO:
- 10+ years of proven expertise
- 500+ satisfied clients pan-India
- 70%+ bid success rate
- Dedicated relationship manager per client
- 24/7 availability during submission deadlines
- Transparent, affordable pricing

CONTACT INFORMATION:
- Phone: +91-9876543210
- Email: info@tenderpro.in
- Office: Ahmedabad, Gujarat (serving pan-India)
- Free consultation available

INSTRUCTIONS:
- Be professional, warm, and helpful
- Reply in the same language the user writes in (Hindi, English, or Hinglish)
- Keep answers concise and easy to understand
- For pricing queries: explain it depends on tender complexity, offer a free consultation call
- Always end by offering further help or suggesting they contact us
- Never fabricate information not listed above
- If a user asks something outside tender services, politely redirect to relevant services
"""

# ─── In-memory session store ──────────────────────────────────────────────────
_session_store: Dict[str, ChatMessageHistory] = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in _session_store:
        _session_store[session_id] = ChatMessageHistory()
    return _session_store[session_id]

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found. Please set it in your .env file.")
    model_name = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    return ChatGroq(
        api_key=api_key,
        model_name=model_name,
        temperature=0.7,
        max_tokens=1024,
    )

# ─── Main AI Response Function ────────────────────────────────────────────────
async def get_ai_response(messages: List[Dict], lead_id: int = None) -> str:
    llm = get_llm()
    session_id = str(lead_id) if lead_id else "anonymous"

    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])

    chain = prompt | llm

    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )

    # Rebuild history from incoming messages (handles page refresh)
    history = get_session_history(session_id)
    if len(messages) > 1:
        history.clear()
        for msg in messages[:-1]:
            if msg["role"] == "user":
                history.add_user_message(msg["content"])
            elif msg["role"] == "assistant":
                history.add_ai_message(msg["content"])

    user_input = messages[-1]["content"] if messages else ""
    if not user_input:
        return "Please send a message."

    response = await chain_with_history.ainvoke(
        {"input": user_input},
        config={"configurable": {"session_id": session_id}},
    )
    return response.content
