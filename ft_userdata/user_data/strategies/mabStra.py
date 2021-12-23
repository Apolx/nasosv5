# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# IMPORTANT: DO NOT USE IT WITHOUT HYPEROPT:
# freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --spaces all --strategy mabStra --config config.json -e 100

# --- Do not remove these libs ---
from freqtrade.strategy.hyper import IntParameter, DecimalParameter
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
# --------------------------------

# Add your lib to import here
import talib.abstract as ta


class mabStra(IStrategy):

    # #################### RESULTS PASTE PLACE ####################
    # ROI table:
    minimal_roi = {
        "0": 0.125,
        "38": 0.053,
        "92": 0.033,
        "135": 0
    }

    # Stoploss:
    stoploss = -0.112
    # Buy hypers
    timeframe = '1m'

    # #################### END OF RESULT PLACE ####################

    # buy params
    buy_mojo_ma_timeframe = IntParameter(2, 100, default=3, space='buy')
    buy_fast_ma_timeframe = IntParameter(2, 100, default=90, space='buy')
    buy_slow_ma_timeframe = IntParameter(2, 100, default=8, space='buy')
    buy_div_max = DecimalParameter(
        0, 2, decimals=4, default=1.7572, space='buy')
    buy_div_min = DecimalParameter(
        0, 2, decimals=4, default=0.0478, space='buy')
    # sell params
    sell_mojo_ma_timeframe = IntParameter(2, 100, default=45, space='sell')
    sell_fast_ma_timeframe = IntParameter(2, 100, default=4, space='sell')
    sell_slow_ma_timeframe = IntParameter(2, 100, default=13, space='sell')
    sell_div_max = DecimalParameter(
        0, 2, decimals=4, default=1.0598, space='sell')
    sell_div_min = DecimalParameter(
        0, 2, decimals=4, default=0.981, space='sell')

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # SMA - ex Moving Average
        dataframe['buy-mojoMA'] = ta.SMA(dataframe,
                                         timeperiod=self.buy_mojo_ma_timeframe.value)
        dataframe['buy-fastMA'] = ta.SMA(dataframe,
                                         timeperiod=self.buy_fast_ma_timeframe.value)
        dataframe['buy-slowMA'] = ta.SMA(dataframe,
                                         timeperiod=self.buy_slow_ma_timeframe.value)
        dataframe['sell-mojoMA'] = ta.SMA(dataframe,
                                          timeperiod=self.sell_mojo_ma_timeframe.value)
        dataframe['sell-fastMA'] = ta.SMA(dataframe,
                                          timeperiod=self.sell_fast_ma_timeframe.value)
        dataframe['sell-slowMA'] = ta.SMA(dataframe,
                                          timeperiod=self.sell_slow_ma_timeframe.value)
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe.loc[
            (
                (dataframe['buy-mojoMA'].div(dataframe['buy-fastMA'])
                    > self.buy_div_min.value) &
                (dataframe['buy-mojoMA'].div(dataframe['buy-fastMA'])
                    < self.buy_div_max.value) &
                (dataframe['buy-fastMA'].div(dataframe['buy-slowMA'])
                    > self.buy_div_min.value) &
                (dataframe['buy-fastMA'].div(dataframe['buy-slowMA'])
                    < self.buy_div_max.value)
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['sell-fastMA'].div(dataframe['sell-mojoMA'])
                    > self.sell_div_min.value) &
                (dataframe['sell-fastMA'].div(dataframe['sell-mojoMA'])
                    < self.sell_div_max.value) &
                (dataframe['sell-slowMA'].div(dataframe['sell-fastMA'])
                    > self.sell_div_min.value) &
                (dataframe['sell-slowMA'].div(dataframe['sell-fastMA'])
                    < self.sell_div_max.value)
            ),
            'sell'] = 1
        return dataframe