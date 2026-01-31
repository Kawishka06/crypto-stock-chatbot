import requests
import pandas as pd
from backend.config import PREDICT_API_BASE

def get_history(asset:str,period_days:int=365) ->pd.DataFrame:
    r=requests.get(f"{PREDICT_API_BASE}/history",params={"asset":asset,"period_days":period_days},timeout=30)
    r.raise_for_status()
    data=r.json()
    df=pd.DataFrame(data["history"])
    df["date"]=pd.to_datetime(df["date"])
    df=df.sort_values("date")

    return df