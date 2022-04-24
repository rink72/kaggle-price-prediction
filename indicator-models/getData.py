import json
import pandas as pd
import pathlib

from malfoy.metatrader.metatrader import Metatrader
from functions.indicators import AddIndicators

# This script updates candle data

candleCount = 5000
instruments = [
  "USDCAD",
  "AUDUSD",
  "USDJPY",
  "USDCHF",
  "EURJPY",
  "GBPUSD",
  "AUDCHF",
  "BTCUSD",
  "TSLA",
  "XAUUSD"
]
granularities = [
  "M5",
  "H1",
  "D1"
]
currentFolder = pathlib.Path(__file__).parent.absolute()
savePath = "{0}/input".format(currentFolder)
metatraderAuthenticationPath = "{0}/metatrader.local.json".format(currentFolder)

jsonFile = open(metatraderAuthenticationPath)
metatraderAuthentication = json.load(jsonFile)
mtApi = Metatrader(**metatraderAuthentication)

for instrument in instruments:
  for granularity in granularities:
    print("Retrieving <{0}> ({1}) candles at <{2}> granularity".format(instrument, candleCount, granularity))
    candles = pd.DataFrame(mtApi.GetCandles(instrument=instrument, granularity=granularity, count=candleCount))

    candles = AddIndicators(data=candles)

    fullFilePath = "{0}/{1}_{2}.csv".format(savePath, instrument, granularity)

    candles.to_csv(fullFilePath)
