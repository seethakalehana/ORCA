
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite"
)
print("ORCA configuration loaded successfully")
print("Gemini API key detected:", bool(GEMINI_API_KEY))

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")
GROQ_API_KEY = os.getenv("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")