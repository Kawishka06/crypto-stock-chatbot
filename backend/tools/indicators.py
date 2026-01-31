import pandas as pd

def sma(series:pd.Series,window:int=14) ->pd.Series:
    return series.rolling(window).mean()

def rsi(series:pd.Series,period:int=14) ->pd.Series:
    delta=series.diff()
    gain= delta.where(delta>0,0.0)
    loss=delta.where(delta<0,0.0)
    avg_gain=gain.rolling(period).mean()
    avg_loss=loss.rolling(period).mean()
    rs=avg_gain/avg_loss.replace(0,1e9)

    return 100- (100/(1+rs))