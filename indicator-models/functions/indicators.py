# Helper functions to add indicator data to instrument pricing
from turtle import update
from typing import KeysView
import pandas_ta as ta
import pandas as pd
from rsa import sign

def AddIndicators(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  # Momentum indicators
  updatedData = AddAOData(data=updatedData)
  updatedData = AddAPOData(data=updatedData)
  updatedData = AddCCIData(data=updatedData)
  updatedData = AddCFOData(data=updatedData)
  updatedData = AddERData(data=updatedData)
  updatedData = AddFisherData(data=updatedData)
  updatedData = AddInertiaData(data=updatedData)
  updatedData = AddKSTData(data=updatedData)
  updatedData = AddMACDData(data=updatedData)
  updatedData = AddMOMData(data=updatedData)
  updatedData = AddPGOData(data=updatedData)
  updatedData = AddPPOData(data=updatedData)
  updatedData = AddPSLData(data=updatedData)
  updatedData = AddROCData(data=updatedData)
  updatedData = AddRSIData(data=updatedData)
  updatedData = AddSlopeData(data=updatedData)
  updatedData = AddSMIData(data=updatedData)

  # TPSL indicators
  updatedData = AddATRData(data=updatedData)

  # Trend indicators
  updatedData = AddAroonData(data=updatedData)
  updatedData = AddKamaData(data=updatedData)

  # Volatility indicators
  updatedData = AddBBandsData(data=updatedData)

  # Volume indicators
  updatedData = AddCMFData(data=updatedData)


  return updatedData

def AddAOData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = AddAOIndicator(data=data)

  return updatedData

def AddAOIndicator(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  ao = ta.ao(updatedData["midHigh"], updatedData["midLow"])
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

  cci = ta.cci(updatedData["midHigh"], updatedData["midLow"], updatedData["midClose"], length)
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

  cfo = ta.cfo(updatedData["midClose"], length)
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

  cg = ta.cg(updatedData["midClose"], length)
  updatedData[key] = cg

  updatedData["bull_signal_{0}".format(key)] = (updatedData[key] > updatedData[key].shift(1)) & (updatedData[key].shift(1) < updatedData[key].shift(2))
  updatedData["bear_signal_{0}".format(key)] = (updatedData[key] < updatedData[key].shift(1)) & (updatedData[key].shift(1) > updatedData[key].shift(2))

def AddERData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  lengthRange = [5, 10, 15]

  for lr in lengthRange:
    updatedData = AddERIndicator(data=updatedData, length=lr)

  return updatedData

def AddERIndicator(data: pd.DataFrame, length: int) -> pd.DataFrame:
  updatedData = data.copy()

  key = "er_{0}".format(length)

  er = ta.er(updatedData["midClose"], length)
  updatedData[key] = er

  updatedData["bull_signal_{0}".format(key)] = (updatedData[key] >= 0.75) & (updatedData[key].shift(1) < 0.75)
  updatedData["bear_signal_{0}".format(key)] = (updatedData[key] <= 0.25) & (updatedData[key].shift(1) > 0.25)

  return updatedData

def AddFisherData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  lengthRange = range(3, 18, 3)
  signalRange = range(1, 4, 1)

  for lr in lengthRange:
    for sr in signalRange:
      updatedData = AddFisherIndicator(data=updatedData, length=lr, signal=sr)

  return updatedData

def AddFisherIndicator(data: pd.DataFrame, length: int, signal: int) -> pd.DataFrame:
  updatedData = data.copy()

  keySuffix = "{0}_{1}".format(length, signal)
  fisherTKey = "fishert_{0}".format(keySuffix)
  fisherSKey = "fishers_{0}".format(keySuffix)

  ft = ta.fisher(
            updatedData["midHigh"],
            updatedData["midLow"],
            length,
            signal
        )

  updatedData[fisherTKey] = ft["FISHERT_{0}".format(keySuffix)]
  updatedData[fisherSKey] = ft["FISHERTs_{0}".format(keySuffix)]

  updatedData["bull_signal_fisher_{0}".format(keySuffix)] = (updatedData[fisherTKey] > updatedData[fisherSKey]) & \
    (updatedData[fisherTKey].shift(1) < updatedData[fisherSKey].shift(1))

  updatedData["bear_signal_fisher_{0}".format(keySuffix)] = (updatedData[fisherTKey] < updatedData[fisherSKey]) & (
            updatedData[fisherTKey].shift(1) > updatedData[fisherSKey].shift(1))

  return updatedData

def AddInertiaData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  maRange = [10, 20, 30]
  rviRange = [7, 14, 21]

  for ma in maRange:
    for rr in rviRange:
      updatedData = AddInertiaIndicator(data=updatedData, movingAverage=ma, rvi=rr)

  return updatedData

def AddInertiaIndicator(data: pd.DataFrame, movingAverage: int, rvi: int) -> pd.DataFrame:
  updatedData = data.copy()

  key = "inertia_{0}_{1}".format(movingAverage, rvi)

  inertia = ta.inertia(updatedData["midClose"], updatedData["midHigh"], updatedData["midLow"], movingAverage, rvi)
  updatedData[key] = inertia

  updatedData["bull_signal_{0}".format(key)] = (updatedData[key] > 50) & (updatedData[key].shift(1) < 50)
  updatedData["bear_signal_{0}".format(key)] = (updatedData[key] < 50) & (updatedData[key].shift(1) > 50)

  return updatedData

def AddKSTData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = AddKSTIndicator(data=data)

  return updatedData

def AddKSTIndicator(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  kst = ta.kst(updatedData["midClose"])
  updatedData["kst"] = kst["KST_10_15_20_30_10_10_10_15"]
  updatedData["ksts"] = kst["KSTs_9"]

  updatedData["bull_signal_kst"] = (updatedData["kst"] > updatedData["ksts"]) & \
    (updatedData["kst"].shift(1) < updatedData["ksts"].shift(1)) & \
      (updatedData["kst"] < 0)

  updatedData["bear_signal_kst"] = (updatedData["kst"] < updatedData["ksts"]) & \
    (updatedData["kst"].shift(1) > updatedData["ksts"].shift(1)) & \
      (updatedData["kst"] > 0)

  return updatedData

def AddMACDData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  fastRange = [6, 12, 18]
  slowRange = [12, 26, 30]
  signalRange = [3, 9, 12]

  for fr in fastRange:
    for sr in slowRange:
        for sigr in signalRange:
          # Make sure we"re not making strategies with garbage indicators
          if (fr < sr) & (sigr < fr):
              updatedData = AddMACDIndicator(data=updatedData, fast=fr, slow=sr, signal=sigr)

  return updatedData

def AddMACDIndicator(data: pd.DataFrame, fast: int, slow: int, signal: int) -> pd.DataFrame:
  updatedData = data.copy()

  keySuffix = "{0}_{1}_{2}".format(fast, slow, signal)
  macdKey = "macd_{0}".format(keySuffix)
  macdHKey = "macdh_{0}".format(keySuffix)
  macdSKey = "macds_{0}".format(keySuffix)

  macd = ta.macd(updatedData["midClose"], fast, slow, signal)

  updatedData[macdKey] = macd["MACD_{0}".format(keySuffix)]
  updatedData[macdHKey] = macd["MACDh_{0}".format(keySuffix)]
  updatedData[macdSKey] = macd["MACDs_{0}".format(keySuffix)]

  updatedData["bull_signal_macd_{0}".format(keySuffix)] = ((updatedData[macdKey] > updatedData[macdSKey]) & \
    (updatedData[macdKey].shift(1) < updatedData[macdSKey].shift(1))) & \
       (updatedData[macdKey] > 0)

  updatedData["bear_signal_macd_{0}".format(keySuffix)] = ((updatedData[macdKey] < updatedData[macdSKey]) & (
            updatedData[macdKey].shift(1) > updatedData[macdSKey].shift(1))) & \
              (updatedData[macdKey] < 0)

  return updatedData

def AddMOMData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  lengthRange = [5, 10]

  for lr in lengthRange:
    updatedData = AddMOMIndicator(data=updatedData, length=lr)

  return updatedData

def AddMOMIndicator(data: pd.DataFrame, length: int) -> pd.DataFrame:
  updatedData = data.copy()

  key = "mom_{0}".format(length)

  mom = ta.mom(updatedData['midClose'], length)
  updatedData[key] = mom

  updatedData["bull_signal_{0}".format(key)] = updatedData[key] > 0
  updatedData["bear_signal_{0}".format(key)] = updatedData[key] < 0

  return updatedData

def AddPGOData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  pgoRange = [7, 14, 21]
  thresholdRange = [0, 2, 3]

  for pr in pgoRange:
    for tr in thresholdRange:
      updatedData = AddPGOIndicator(data=updatedData, pgo=pr, threshold=tr)

  return updatedData

def AddPGOIndicator(data: pd.DataFrame, pgo: int, threshold: int) -> pd.DataFrame:
  updatedData = data.copy()

  key = "pgo_{0}_{1}".format(pgo, threshold)

  pgo = ta.pgo(updatedData['midHigh'], updatedData['midLow'], updatedData['midClose'], pgo)
  updatedData[key] = pgo

  updatedData["bull_signal_{0}".format(key)] = (updatedData[key] > threshold) & \
    (updatedData[key].shift(1) < threshold)

  updatedData["bear_signal_{0}".format(key)] = (updatedData[key] < -threshold) & \
    (updatedData[key].shift(1) > -threshold)

  return updatedData

def AddPPOData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  fastRange = [6, 12, 18]
  slowRange = [13, 26, 30]
  signalRange = [3, 9, 12]

  for fr in fastRange:
    for sr in slowRange:
        for sigr in signalRange:
          if (fr < sr) & (sigr < fr):
            updatedData = AddPPOIndicator(data=updatedData, fast=fr, slow=sr, signal=sigr)

  return updatedData

def AddPPOIndicator(data: pd.DataFrame, fast: int, slow: int, signal: int) -> pd.DataFrame:
  updatedData = data.copy()

  keySuffix = "{0}_{1}_{2}".format(fast, slow, signal)
  ppoKey = "ppo_{0}".format(keySuffix)
  ppoHKey = "ppoh_{0}".format(keySuffix)
  ppoSKey = "ppos_{0}".format(keySuffix)

  ppo = ta.ppo(updatedData['midClose'], fast, slow, signal)

  updatedData[ppoKey] = ppo["PPO_{0}".format(keySuffix)]
  updatedData[ppoHKey] = ppo["PPOh_{0}".format(keySuffix)]
  updatedData[ppoSKey] = ppo["PPOs_{0}".format(keySuffix)]

  updatedData["bull_signal_{0}".format(ppoKey)] = (updatedData[ppoKey] > updatedData[ppoSKey]) & \
    (updatedData[ppoKey].shift(1) < updatedData[ppoSKey].shift(1))

  updatedData["bear_signal_{0}".format(ppoKey)] = (updatedData[ppoKey] < updatedData[ppoSKey]) & \
    (updatedData[ppoKey].shift(1) > updatedData[ppoSKey].shift(1))

  return updatedData

def AddPSLData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  pslRange = [6, 12, 20]

  for pr in pslRange:
    updatedData = AddPSLIndicator(data=updatedData, psl=pr)

  return updatedData

def AddPSLIndicator(data: pd.DataFrame, psl: int) -> pd.DataFrame:
  updatedData = data.copy()

  key = "psl_{0}".format(psl)

  psl = ta.psl(updatedData['midClose'], length=psl)
  updatedData[key] = psl

  updatedData["bull_signal_{0}".format(key)] = (updatedData[key] > 50) & \
    (updatedData[key].shift(1) <= 50)

  updatedData["bear_signal_{0}".format(key)] = (updatedData[key] < 50) & \
    (updatedData[key].shift(1) >= 50)

  return updatedData

def AddROCData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  rocRange = [3, 6, 9, 12]

  for rr in rocRange:
    updatedData = AddROCIndicator(data=updatedData, roc=rr)

  return updatedData

def AddROCIndicator(data: pd.DataFrame, roc: int):
  updatedData = data.copy()

  key = "roc_{0}".format(roc)

  roc = ta.roc(updatedData['midClose'], roc)
  updatedData[key] = roc

  updatedData["bull_signal_{0}".format(key)] = (updatedData[key] > 0) & \
    (updatedData[key].shift(1) <= 0)

  updatedData["bear_signal_{0}".format(key)] = (updatedData[key] < 0) & \
    (updatedData[key].shift(1) >= 0)

  return updatedData

def AddRSIData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  rsiRange = [7, 14, 21]

  for rr in rsiRange:
    updatedData = AddRSIIndicator(data=updatedData, rsi=rr)

  return updatedData

def AddRSIIndicator(data: pd.DataFrame, rsi: int) -> pd.DataFrame:
  updatedData = data.copy()

  key = "rsi_{0}".format(rsi)

  rsi = ta.rsi(updatedData['midClose'], rsi)
  updatedData[key] = rsi

  updatedData["bull_signal_{0}".format(key)] = (updatedData[key] > 30) & \
    (updatedData[key].shift(1) <= 30)

  updatedData["bear_signal_{0}".format(key)] = (updatedData[key] < 70) & \
    (updatedData[key].shift(1) >= 70)

  return updatedData

def AddSlopeData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  slopeRange = [1, 5, 10]

  for sr in slopeRange:
    updatedData = AddSlopeIndicator(data=updatedData, slope=sr)

  return updatedData

def AddSlopeIndicator(data: pd.DataFrame, slope: int) -> pd.DataFrame:
  updatedData = data.copy()

  key = "slope_{0}".format(slope)

  slope = ta.slope(updatedData['midClose'], slope)
  updatedData[key] = slope

  updatedData["bull_signal_{0}".format(key)] = (updatedData[key] > 0) & \
    (updatedData[key].shift(1) <= 0)

  updatedData["bear_signal_{0}".format(key)] = (updatedData[key] < 0) & \
    (updatedData[key].shift(1) >= 0)

  return updatedData

def AddSMIData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  fastRange = [2, 5, 12]
  slowRange = [13, 20, 30]
  signalRange = [2, 5, 12]

  for fr in fastRange:
    for sr in slowRange:
        for sigr in signalRange:
          if (fr < sr) & (sigr < fr):
            updatedData = AddSMIIndicator(data=updatedData, fast=fr, slow=sr, signal=sigr)

  return updatedData

def AddSMIIndicator(data: pd.DataFrame, fast: int, slow: int, signal: int) -> pd.DataFrame:
  updatedData = data.copy()

  keySuffix = "{0}_{1}_{2}".format(fast, slow, signal)
  smiKey = "smi_{0}".format(keySuffix)
  smiSKey = "smis_{0}".format(keySuffix)
  smiOKey = "smio_{0}".format(keySuffix)

  smi = ta.smi(updatedData['midClose'], fast, slow, signal)
  updatedData[smiKey] = smi["SMI_" + keySuffix]
  updatedData[smiSKey] = smi["SMIs_" + keySuffix]
  updatedData[smiOKey] = smi["SMIo_" + keySuffix]

  updatedData["bull_signal_{0}".format(smiKey)] = (updatedData[smiKey] > updatedData[smiSKey]) & \
    (updatedData[smiKey].shift(1) < updatedData[smiSKey].shift(1))

  updatedData["bear_signal_{0}".format(smiKey)] = (updatedData[smiKey] < updatedData[smiSKey]) & \
    (updatedData[smiKey].shift(1) > updatedData[smiSKey].shift(1))

  return updatedData

def AddATRData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = AddATRIndicator(data=data)

  return updatedData

def AddATRIndicator(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  key = "atr"

  atr = ta.atr(updatedData["midHigh"], updatedData["midLow"], updatedData["midClose"])
  updatedData[key] = atr

  return updatedData

def AddAroonData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  lengthRange = [7, 14, 21]

  for lr in lengthRange:
    updatedData = AddAroonIndicator(data=updatedData, length=lr)

  return updatedData

def AddAroonIndicator(data: pd.DataFrame, length: int) -> pd.DataFrame:
  updatedData = data.copy()

  keySuffix = "{0}".format(length)
  aroonUKey = "aroonu_{0}".format(keySuffix)
  aroonDKey = "aroond_{0}".format(keySuffix)

  aroon = ta.aroon(updatedData["midHigh"], updatedData["midLow"], length)
  updatedData[aroonUKey] = aroon["AROONU_" + keySuffix]
  updatedData[aroonDKey] = aroon["AROOND_" + keySuffix]

  updatedData["bull_signal_aroon_{0}".format(keySuffix)] = updatedData[aroonUKey] > 80
  updatedData["bear_signal_aroon_{0}".format(keySuffix)] = updatedData[aroonDKey] > 80

  return updatedData

def AddKamaData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  fastRange = range(5, 21, 5)
  slowRange = range(10, 31, 10)
  periodRange = [7, 14, 26, 52]

  for fr in fastRange:
    for sr in slowRange:
        for per in periodRange:
          updatedData = AddKamaIndicator(data=updatedData, fast=fr, slow=sr, period=per)

  return updatedData

def AddKamaIndicator(data: pd.DataFrame, fast: int, slow: int, period: int) -> pd.DataFrame:
  updatedData = data.copy()

  key = "kama_{0}_{1}_{2}".format(fast, slow, period)

  kama = ta.kama(updatedData["midClose"], period, fast, slow)
  updatedData[key] = kama

  updatedData["bull_signal_{0}".format(key)] = (updatedData[key] > updatedData["midClose"]) & \
    (updatedData[key].shift(1) < updatedData["midClose"].shift(1))

  updatedData["bear_signal_{0}".format(key)] = (updatedData[key] < updatedData["midClose"]) & \
    (updatedData[key].shift(1) > updatedData["midClose"].shift(1))

  return updatedData

def AddBBandsData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  bollRange = range(5, 20, 5)

  for br in bollRange:
    updatedData = AddBBandsIndicator(data=updatedData, movingAverage=br)

  return updatedData

def AddBBandsIndicator(data: pd.DataFrame, movingAverage: int) -> pd.DataFrame:
  updatedData = data.copy()

  keySuffix = "{0}".format(movingAverage)
  bbandsLKey = "bbandsl_{0}".format(keySuffix)
  bbandsMKey = "bbandsm_{0}".format(keySuffix)
  bbandsUKey = "bbandsu_{0}".format(keySuffix)

  bb = ta.bbands(updatedData["midClose"], movingAverage, 2)
  updatedData[bbandsLKey] = bb["BBL_{0}_2.0".format(keySuffix)]
  updatedData[bbandsMKey] = bb["BBM_{0}_2.0".format(keySuffix)]
  updatedData[bbandsUKey] = bb["BBU_{0}_2.0".format(keySuffix)]

  updatedData["bull_signal_bbands_{0}".format(keySuffix)] = (updatedData["midClose"] > updatedData[bbandsMKey]) & \
    (updatedData["midClose"].shift(1) < updatedData[bbandsMKey].shift(1))

  updatedData["bear_signal_bbands_{0}".format(keySuffix)] = (updatedData["midClose"] < updatedData[bbandsMKey]) & \
    (updatedData["midClose"].shift(1) > updatedData[bbandsMKey].shift(1))

  return updatedData

def AddCMFData(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = AddCMFIndicator(data=data)

  return updatedData

def AddCMFIndicator(data: pd.DataFrame) -> pd.DataFrame:
  updatedData = data.copy()

  key = "cmf"

  cmf = ta.cmf(updatedData["midHigh"], updatedData["midLow"], updatedData["midClose"], updatedData["volume"])
  updatedData["cmf"] = cmf

  return updatedData