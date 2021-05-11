import talib.abstract as ta
from pandas import DataFrame
from typing import Dict, Any, Callable, List
from functools import reduce
from skopt.space import Categorical, Dimension, Integer, Real
import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.optimize.hyperopt_interface import IHyperOpt

__author__      = "Robert Roman"
__credits__     = ["Bloom Trading, Mohsen Hassan - thanks for teaching me Freqtrade!"]
__copyright__   = "Free For Use"
__license__     = "MIT"
__version__     = "1.0"
__maintainer__  = "Robert Roman"
__email__       = "robertroman7@gmail.com"

class bbrsi_opt(IHyperOpt):

    @staticmethod
    def stoploss_space() -> List[Dimension]:
        return [
            Real(-0.15, -0.02, name='stoploss'),
        ]

    @staticmethod
    def buy_strategy_generator(params: Dict[str, Any]) -> Callable:
        def populate_buy_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            conditions = []
            
            # GUARDS AND TRENDS
            if 'rsi-enabled' in params and params['rsi-enabled']:
                conditions.append(dataframe['rsi'] > params['rsi-value'])
            if 'mfi-enabled' in params and params['mfi-enabled']:
                conditions.append(dataframe['mfi'] > params['mfi-value'])

            # TRIGGERS
            if 'trigger' in params:
                if params['trigger'] == 'bb_lower1':
                    conditions.append(dataframe["close"] < dataframe['bb_lowerband1'])
                if params['trigger'] == 'bb_lower2':
                    conditions.append(dataframe["close"] < dataframe['bb_lowerband2'])
                if params['trigger'] == 'bb_lower3':
                    conditions.append(dataframe["close"] < dataframe['bb_lowerband3'])
                if params['trigger'] == 'bb_lower4':
                    conditions.append(dataframe["close"] < dataframe['bb_lowerband4'])

            # Check that volume is not 0
            conditions.append(dataframe['volume'] > 0)

            if not conditions:
                pass
            else:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'buy'] = 1

            return dataframe

        return populate_buy_trend

    @staticmethod
    def indicator_space() -> List[Dimension]:
        return [
            Integer(10, 60, name='rsi-value'),
            Integer(10, 60, name='mfi-value'),
            Categorical([True, False], name='rsi-enabled'),
            Categorical([True, False], name='mfi-enabled'),
            Categorical(['bb_lower1','bb_lower2','bb_lower3','bb_lower4'], name='trigger')
        ]

    @staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:
        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            conditions = []
            
            # GUARDS AND TRENDS
            if 'sell-rsi-enabled' in params and params['sell-rsi-enabled']:
                conditions.append(dataframe['rsi'] > params['sell-rsi-value'])
            if 'sell-mfi-enabled' in params and params['sell-mfi-enabled']:
                conditions.append(dataframe['mfi'] > params['sell-mfi-value'])

            # TRIGGERS
            if 'sell-trigger' in params:
                if params['sell-trigger'] == 'sell-bb_upper1':
                    conditions.append(dataframe["close"] > dataframe['bb_upperband1'])
                if params['sell-trigger'] == 'sell-bb_upper2':
                    conditions.append(dataframe["close"] > dataframe['bb_upperband2'])
                if params['sell-trigger'] == 'sell-bb_upper3':
                    conditions.append(dataframe["close"] > dataframe['bb_upperband3'])
                if params['sell-trigger'] == 'sell-bb_upper4':
                    conditions.append(dataframe["close"] > dataframe['bb_upperband4'])

            # Check that volume is not 0
            conditions.append(dataframe['volume'] > 0)

            if not conditions:
                pass
            else:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell'] = 1

            return dataframe

        return populate_sell_trend

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:
        return [
            Integer(50, 90, name='sell-rsi-value'),
            Integer(50, 90, name='sell-mfi-value'),
            Categorical([True, False], name='sell-rsi-enabled'),
            Categorical([True, False], name='sell-mfi-enabled'),
            Categorical(['sell-bb_upper1','sell-bb_upper2','sell-bb_upper3','sell-bb_upper4'], name='sell-trigger')
        ]
