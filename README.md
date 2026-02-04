# 🤖 AI-Powered Market Chatbot

A **tool-augmented conversational AI** that provides interpretable stock and crypto market insights by combining machine learning forecasts, technical indicators, and natural language interaction.

Unlike traditional chatbots, this system does **not hallucinate** market data.  
All responses are grounded in **real model outputs and indicators**.

---

## 🔹 Key Capabilities

- Conversational interface for market analysis
- Uses real ML predictions from the forecasting API
- Dynamically computes technical indicators:
  - RSI
  - SMA
- Intent-aware responses:
  - Trend analysis
  - Buy / wait reasoning
  - Indicator explanations
  - Forecast interpretation
- Designed to integrate with LLMs (OpenAI) or run in mock mode

---

## 🧠 Architecture Overview

The chatbot:
- Calls tools to fetch real data
- Builds structured context
- Generates responses based on **user intent + market state**

---

## 🛠️ Tech Stack

- Python
- FastAPI
- REST APIs
- Tool-based reasoning
- Optional OpenAI API integration

---

## ▶️ Run Locally

```bash
uvicorn backend.main:app --reload --port 8000

Health Check:
http://localhost:8000/health

API docs:
http://localhost:8000/docs
