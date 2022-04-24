# Helper functions to add indicator data to instrument pricing
from turtle import update
import pandas_ta as ta
import pandas as pd

def AddIndicators(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  updatedData = AddAOData(data=updatedData)

  return updatedData

def AddAOData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  ao = ta.ao(updatedData['midHigh'], updatedData['midLow'])
  updatedData["ao"] = ao

  updatedData["bull_signal_ao"] = (updatedData["ao"] > 0) & (updatedData["ao"].shift(1) < 0)
  updatedData["bear_signal_ao"] = (updatedData["ao"] < 0) & (updatedData["ao"].shift(1) > 0)

  return updatedData