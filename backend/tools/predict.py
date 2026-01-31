import requests
from backend.config import PREDICT_API_BASE

def get_forecast(asset:str, horizon:int=7) -> dict:
    r=requests.get(f"{PREDICT_API_BASE}/predict",params={"asset":asset,"horizon":horizon},timeout=60)
    r.raise_for_status()
    return r.json()