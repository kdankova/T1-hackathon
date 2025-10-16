import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))

STREAMLIT_THEME = {
    "primaryColor": "#1f77b4",
    "backgroundColor": "#ffffff",
    "secondaryBackgroundColor": "#f0f2f6",
    "textColor": "#262730",
    "font": "sans serif"
}

