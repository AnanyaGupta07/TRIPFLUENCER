import os
import textwrap
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from dotenv import load_dotenv
import google.generativeai as genai

# -------------------------
# ENV SETUP
# -------------------------
PROJECT_DIR = os.path.dirname(__file__)
ENV_PATH = os.path.join(PROJECT_DIR, ".env")
load_dotenv(dotenv_path=ENV_PATH, override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

SELECTED_MODEL: Optional[str] = None


def select_flash_model() -> Optional[str]:
    try:
        models = list(genai.list_models())
        candidates = [
            m.name for m in models
            if "flash" in m.name and hasattr(m, "supported_generation_methods") and
               ("generateContent" in m.supported_generation_methods or "generate_content" in m.supported_generation_methods)
        ]

        preference = [
            "models/gemini-1.5-flash",
            "models/gemini-1.5-flash-latest",
            "models/gemini-1.5-flash-002",
            "models/gemini-1.5-flash-001",
            "models/gemini-1.5-flash-8b",
            "gemini-1.5-flash",
        ]

        for p in preference:
            if p in candidates:
                return p
        return candidates[0] if candidates else None
    except Exception:
        return None


SELECTED_MODEL = select_flash_model() or "models/gemini-1.5-flash"

# -------------------------
# FASTAPI APP
# -------------------------
app = FastAPI(title="TripFluencer AI Itinerary Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# STATIC + TEMPLATE SETUP
# -------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# -------------------------
# ROUTES
# -------------------------
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/favicon.ico")
async def favicon():
    return Response(content=b"", media_type="image/x-icon", status_code=200)


@app.post("/generate")
async def generate(payload: Dict[str, Any]):
    load_dotenv(dotenv_path=ENV_PATH, override=True)
    api_key = os.getenv("GEMINI_API_KEY", "")

    if not api_key:
        raise HTTPException(status_code=400, detail="Missing GEMINI_API_KEY")

    genai.configure(api_key=api_key)

    source = (payload or {}).get("source", "").strip()
    destination = (payload or {}).get("destination", "").strip()
    people = (payload or {}).get("people", "").strip()
    duration = int((payload or {}).get("duration", 0) or 0)
    interests = (payload or {}).get("interests", "").strip()
    budget = (payload or {}).get("budget", "").strip() or "Mid-range"
    extras = (payload or {}).get("extras", "").strip()

    if not source or not destination or duration <= 0 or not people:
        raise HTTPException(
            status_code=400,
            detail="source, destination, duration (>0), and people are required"
        )

    model_name = select_flash_model() or SELECTED_MODEL

    instructions = textwrap.dedent("""
    You are an expert travel planner. Generate a comprehensive, personalized itinerary.
    FORMAT:
    - Markdown headings
    - High-Level Overview
    - Day-by-Day Itinerary
    - Cost Breakdown
    - Practical Tips
    """)

    user_context = f"""
    Source: {source}
    Destination: {destination}
    People: {people}
    Duration: {duration} days
    Interests: {interests or 'N/A'}
    Budget: {budget}
    Extras: {extras or 'N/A'}
    """

    prompt = f"{instructions}\n\nUser Inputs:\n{user_context}"

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        text = (getattr(response, "text", "") or "").strip()

        if not text:
            raise HTTPException(status_code=502, detail="Empty response from Gemini")

        return JSONResponse({"markdown": text, "model": model_name})

    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Generation failed: {exc}")