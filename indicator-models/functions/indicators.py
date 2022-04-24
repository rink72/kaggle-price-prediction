# Helper functions to add indicator data to instrument pricing
from turtle import update
import pandas_ta as ta
import pandas as pd

def AddIndicators(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  updatedData = AddAOData(data=updatedData)
  updatedData = AddAPOData(data=updatedData)

  return updatedData

def AddAOData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = AddAOIndicator(data=data)

  return updatedData

def AddAOIndicator(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  ao = ta.ao(updatedData['midHigh'], updatedData['midLow'])
  updatedData["ao"] = ao

  updatedData["bull_signal_ao"] = (updatedData["ao"] > 0) & (updatedData["ao"].shift(1) < 0)
  updatedData["bear_signal_ao"] = (updatedData["ao"] < 0) & (updatedData["ao"].shift(1) > 0)

  return updatedData

def AddAPOData(data: pd.DataFrame):
  updatedData = data.copy()

  fastRange = range(5, 30, 5)
  slowRange = range(10, 60, 5)

  paramList = []

  for fr in fastRange:
      for sr in slowRange:
        if fr < sr:
          updatedData = AddAPOIndicator(data=updatedData, apoFast=fr, apoSlow=sr)

  return updatedData

def AddAPOIndicator(data: pd.DataFrame, apoFast: int, apoSlow: int):
  updatedData = data.copy()

  key = "apo_{0}_{1}".format(apoFast, apoSlow)

  apo = ta.apo(updatedData["midClose"], apoFast, apoSlow)
  updatedData[key] = apo

  updatedData["bull_signal_{0}".format(key)] = (updatedData[key] > 0) & (updatedData[key].shift(1) < 0)
  updatedData["bear_signal_{0}".format(key)] = (updatedData[key] < 0) & (updatedData[key].shift(1) > 0)

  return updatedData