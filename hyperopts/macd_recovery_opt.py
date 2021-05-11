import talib.abstract as ta
from pandas import DataFrame
from typing import Dict, Any, Callable, List
import numpy as np
from skopt.space import Categorical, Dimension, Integer, Real
import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.optimize.hyperopt_interface import IHyperOpt

__author__      = "Robert Roman"
__copyright__   = "Free For Use"
__license__     = "MIT"
__version__     = "1.0"
__maintainer__  = "Robert Roman"
__email__       = "robertroman7@gmail.com"

class MACD200OPT(IHyperOpt):

    @staticmethod
    def stoploss_space() -> List[Dimension]:

        return [
            Real(-0.15, -0.01, name='stoploss'),
        ]

    @staticmethod
    def generate_roi_table(params: Dict) -> Dict[int, float]:

        roi_table = {}
        roi_table[0] = params['roi_p1'] + params['roi_p2'] + params['roi_p3'] + params['roi_p4'] + params['roi_p5'] + params['roi_p6'] + params['roi_p7'] + params['roi_p8'] + params['roi_p9'] + params['roi_p10']
        roi_table[params['roi_t10']] = params['roi_p1'] + params['roi_p2'] + params['roi_p3'] + params['roi_p4'] + params['roi_p5'] + params['roi_p6'] + params['roi_p7'] + params['roi_p8'] + params['roi_p9']
        roi_table[params['roi_t10'] + params['roi_t9']] = params['roi_p1'] + params['roi_p2'] + params['roi_p3'] + params['roi_p4'] + params['roi_p5'] + params['roi_p6'] + params['roi_p7'] + params['roi_p8']
        roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8']] = params['roi_p1'] + params['roi_p2'] + params['roi_p3'] + params['roi_p4'] + params['roi_p5'] + params['roi_p6'] + params['roi_p7']
        roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8'] + params['roi_t7']] = params['roi_p1'] + params['roi_p2'] + params['roi_p3'] + params['roi_p4'] + params['roi_p5'] + params['roi_p6']
        roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8'] + params['roi_t7'] + params['roi_t6']] = params['roi_p1'] + params['roi_p2'] + params['roi_p3'] + params['roi_p4'] + params['roi_p5']
        roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8'] + params['roi_t7'] + params['roi_t6'] + params['roi_t5']] = params['roi_p1'] + params['roi_p2'] + params['roi_p3'] + params['roi_p4']
        roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8'] + params['roi_t7'] + params['roi_t6'] + params['roi_t5'] + params['roi_t4']] = params['roi_p1'] + params['roi_p2'] + params['roi_p3']
        roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8'] + params['roi_t7'] + params['roi_t6'] + params['roi_t5'] + params['roi_t4'] + params['roi_t3']] = params['roi_p1'] + params['roi_p2']
        roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8'] + params['roi_t7'] + params['roi_t6'] + params['roi_t5'] + params['roi_t4'] + params['roi_t3'] + params['roi_t2']] = params['roi_p1']
        roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8'] + params['roi_t7'] + params['roi_t6'] + params['roi_t5'] + params['roi_t4'] + params['roi_t3'] + params['roi_t2'] + params['roi_t1']] = 0

        return roi_table

    @staticmethod
    def roi_space() -> List[Dimension]:

        return [
            Integer(1, 300, name='roi_t10'),
            Integer(1, 300, name='roi_t9'),
            Integer(1, 300, name='roi_t8'),
            Integer(1, 300, name='roi_t7'),
            Integer(1, 300, name='roi_t6'),
            Integer(1, 300, name='roi_t5'),
            Integer(1, 300, name='roi_t4'),
            Integer(1, 300, name='roi_t3'),
            Integer(1, 300, name='roi_t2'),
            Integer(1, 300, name='roi_t1'),

            Real(0.001, 0.005, name='roi_p10'),
            Real(0.001, 0.005, name='roi_p9'),
            Real(0.001, 0.005, name='roi_p8'),
            Real(0.001, 0.005, name='roi_p7'),
            Real(0.001, 0.005, name='roi_p6'),
            Real(0.001, 0.005, name='roi_p5'),
            Real(0.001, 0.005, name='roi_p4'),
            Real(0.001, 0.005, name='roi_p3'),
            Real(0.0001, 0.005, name='roi_p2'),
            Real(0.0001, 0.005, name='roi_p1'),
        ]

    @staticmethod
    def buy_strategy_generator(params: Dict[str, Any]) -> Callable:
        def populate_buy_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            dataframe.loc[
                (
                        (dataframe['rsi'].rolling(8).min() < params['buy-rsi-value']) &
                        (dataframe['close'] > dataframe['ema200']) &
                        (qtpylib.crossed_above(dataframe['macd'], dataframe['macdsignal']))
                ),
                'buy'] = 1

            return dataframe

        return populate_buy_trend

    @staticmethod
    def indicator_space() -> List[Dimension]:
        return [
            Integer(0, 50, name='buy-rsi-value'),
        ]

    @staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:
        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            dataframe.loc[
                (
                        (dataframe['rsi'].rolling(8).max() > params['sell-rsi-value']) &
                        (dataframe['macd'] > 0) &
                        (qtpylib.crossed_below(dataframe['macd'], dataframe['macdsignal']))
                ),
                'sell'] = 1

            return dataframe

        return populate_sell_trend

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:
        return [
            Integer(50, 100, name='sell-rsi-value'),
        ]
