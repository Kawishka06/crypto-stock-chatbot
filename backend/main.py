from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from backend.llm import generate_reply

from backend.schemas import ChatRequest, ChatResponse
from backend.tools.market_data import get_history
from backend.tools.indicators import sma, rsi
from backend.tools.predict import get_forecast

app = FastAPI(title="Market Chatbot API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return{"status":"ok"}

@app.post("/chat",response_model=ChatResponse)
def chat(req:ChatRequest):
    user_msg=""
    for m in reversed(req.messages):
        user_msg=m.content
        break
    
    asset=(req.asset or "BTC-USD").upper()
    horizon=int(req.horizon or 7)

    try:
        forecast= get_forecast(asset,horizon=horizon)
        hist=get_history(asset,period_days=365)
        close=hist["close"].astype(float)

        sma_14 = float(sma(close, 14).iloc[-1])
        sma_50 = float(sma(close, 50).iloc[-1]) if len(close) >= 50 else None
        rsi_14 = float(rsi(close, 14).iloc[-1])

        last_value=float(forecast["last_value"])
        last_date=forecast["last_date"]
        preds=forecast["predictions"]

        trend = "bullish" if sma_50 and sma_14 > sma_50 else "neutral/bearish"
        next7 = preds[-1]["yhat"] if preds else None

        context = {
            "asset": asset,
            "horizon": horizon,
            "last_value": last_value,
            "last_date": last_date,
            "rsi_14": rsi_14,
            "sma_14": sma_14,
            "sma_50": sma_50,
            "trend": trend,
            "next_end": next7,
        }

        reply = generate_reply(user_msg, context)
        
        return ChatResponse(
            reply=reply,
            tool_calls=[
                {"tool": "get_forecast", "asset": asset, "horizon": horizon},
                {"tool": "get_history", "asset": asset, "period_days": 365},
                {"tool": "indicators", "sma14": sma_14, "rsi14": rsi_14},
            ],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))