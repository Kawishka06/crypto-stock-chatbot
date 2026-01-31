import os

PREDICT_API_BASE = os.getenv("PREDICT_API_BASE", "https://crypto-and-stock.onrender.com")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")