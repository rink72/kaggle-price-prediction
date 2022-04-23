# kaggle-price-prediction

This repo tries to replicate the results from some published notebooks on kaggle that perform price prediction.

## Notebook 1

This can be found [here](https://www.kaggle.com/code/ysthehurricane/bitcoin-dogecoin-etc-price-prediction-xgboost/notebook) and the recreation and extensions can be found [here](./notebook1/)

## Added features notebooks

This notebook is my own creation where I will try and investigate the following:

- Price and price deltas are likely not going to be very informative. Looking at any examples online that do this, they run in to the same problem that I have where the models just learn that the least error is to just predict something close to the previous price. When looking at if they actually predict the delta correctly, it's almost just noise.
- We can look at using the [pandas_ta](https://github.com/twopirllc/pandas-ta) package to add a bunch of different indicators (reference previous malfoy work for this)
- When adding new indicators, it's likely the delta values will be more useful but will need to check this on a case by case basis
- Rather than absolute difference, we may also want to look at percentage difference. For some instruments, they may stay within a specific range of values but for others they may continue to increase in value, making absolute difference mean less
- We may be able to use the work from malfoy of custom indicators to add a *lot* more information and then see if any of it is useful
- We could also look at adding in the work from [forex-resistance-testing](https://dev.azure.com/rink72/Ideas/_git/IDEA-20-forex-resistance) to identify if the price is in a support/resistance area
- Look at applying some of the approaches from [here](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook)
- All notebooks should be written to make it easy to change instrument, granularity, and prediction timesteps

### Possible targets for prediction

- price delta - This would be a starting point only. Prediciting the actual price change is not likely to be accurate
- price direction - This might be easier to predict and allow trading strategies where you are already in a trend and can use it to enter and maintain a trade until it bounces
- large price movements - A classification model where moves of a multiple of ATR or percentage are predicted.
- Highs/Lows - Again not likely to be accurate but be interesting to see
- ATR - Predict the upcoming ATR
- Volume - Predict the upcoming volume
- Trade entries - manually create a dataset where entering trades would be profitable and see if the model can learn from that. Guess this would be a classification model? -1 -> sell, 0 no action, 1 -> buy?
### Some indicator ideas

- The basic/obvious ones that you can find when you google indicators on the internet. They are all available in [pandas_ta](https://github.com/twopirllc/pandas-ta)
- Some custom indicators I created in [malfoy](https://dev.azure.com/rink72/malfoy/_git/malfoy.core)
- above or below EMA by ATR. ie 1.2 if the current price is 120% of the ATR above or below the EMA. -1.2 if it's 120% below
- Most delta's should be percentage based, not absolutes
- We could extend the resistance/support work done [here](https://dev.azure.com/rink72/Ideas/_git/IDEA-20-forex-resistance) and have metadata about each area.
  - Once leaving the area, the percentage of time it goes positive or negative etc. This could become another feature(s)
  - Would require more work and something to add later on if initial work is promising