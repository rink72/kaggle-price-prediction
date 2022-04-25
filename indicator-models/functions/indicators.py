# Helper functions to add indicator data to instrument pricing
from turtle import update
import pandas_ta as ta
import pandas as pd

def AddIndicators(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  updatedData = AddAOData(data=updatedData)
  updatedData = AddAPOData(data=updatedData)
  updatedData = AddCCIData(data=updatedData)
  updatedData = AddCFOData(data=updatedData)

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

def AddCCIData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  lengthRange = range(10, 41, 10)

  for lr in lengthRange:
    updatedData = AddCCIIndicator(data=updatedData, length=lr)

  return updatedData

def AddCCIIndicator(data: pd.DataFrame, length: int) -> pd.DataFrame:
  updatedData = data.copy()

  key = "cci_{0}".format(length)

  cci = ta.cci(updatedData['midHigh'], updatedData['midLow'], updatedData['midClose'], length)
  updatedData[key] = cci

  updatedData["bull_signal_{0}".format(key)] = (updatedData[key] >= 100) & (updatedData[key].shift(1) < 100)
  updatedData["bear_signal_{0}".format(key)] = (updatedData[key] <= -100) & (updatedData[key].shift(1) > -100)

  return updatedData

def AddCFOData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  lengthRange = [7, 14, 21, 28]

  for lr in lengthRange:
    updatedData = AddCFOIndicator(data=updatedData, length=lr)

  return updatedData

def AddCFOIndicator(data: pd.DataFrame, length: int) -> pd.DataFrame:
  updatedData = data.copy()

  key = "cfo_{0}".format(length)

  cfo = ta.cfo(updatedData['midClose'], length)
  updatedData[key] = cfo

  updatedData["bull_signal_{0}".format(key)] = (updatedData[key] >= 0) & (updatedData[key].shift(1) < 0)
  updatedData["bear_signal_{0}".format(key)] = (updatedData[key] <= 0) & (updatedData[key].shift(1) > 0)

  return updatedData

def AddCGData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  lengthRange = [5, 10, 20, 30, 40]

  for lr in lengthRange:
    updatedData = AddCGIndicator(data=updatedData, length=lr)

  return updatedData

def AddCGIndicator(data: pd.DataFrame, length: int) -> pd.DataFrame:
  updatedData = data.copy()

  key = "cg_{0}".format(length)

  cg = ta.cg(updatedData['midClose'], length)
  updatedData[key] = cg

  updatedData["bull_signal_{0}".format(key)] = (updatedData[key] > updatedData[key].shift(1)) & (updatedData[key].shift(1) < updatedData[key].shift(2))
  updatedData["bear_signal_{0}".format(key)] = (updatedData[key] < updatedData[key].shift(1)) & (updatedData[key].shift(1) > updatedData[key].shift(2))