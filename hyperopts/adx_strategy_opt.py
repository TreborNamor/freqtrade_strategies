from functools import reduce
from typing import Any, Callable, Dict, List
import numpy as np
import pandas as pd
from pandas import DataFrame
from skopt.space import Categorical, Dimension, Integer, Real
from freqtrade.optimize.hyperopt_interface import IHyperOpt
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

__author__      = "Robert Roman"
__copyright__   = "Free For Use"
__license__     = "MIT"
__version__     = "1.0"
__maintainer__  = "Robert Roman"
__email__       = "robertroman7@gmail.com"

class adx_strategy_opt(IHyperOpt):

    @staticmethod
    def buy_strategy_generator(params: Dict[str, Any]) -> Callable:
        def populate_buy_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            conditions = []

            # GUARDS AND TRENDS
            if params.get('adx-enabled'):
                conditions.append(dataframe['adx'] > params['adx-value'])
            if params.get('plus-enabled'):
                conditions.append(dataframe['plus_di'] > params['plus_di-value'])
            if params.get('minus-enabled'):
                conditions.append(dataframe['minus_di'] > params['minus_di-value'])

            # TRIGGERS
            if 'trigger' in params:
                if params['trigger'] == 'buy_signal':
                    conditions.append(qtpylib.crossed_above(dataframe['minus_di'], dataframe['plus_di']))

            conditions.append(dataframe['volume'] > 0)

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'buy'] = 1

            return dataframe
        return populate_buy_trend

    @staticmethod
    def indicator_space() -> List[Dimension]:
        return [
            Integer(0, 40, name='adx-value'),
            Integer(0, 40, name='plus_di-value'),
            Integer(0, 40, name='minus_di-value'),
            Categorical([True, False], name='adx-enabled'),
            Categorical([True, False], name='plus_di-enabled'),
            Categorical([True, False], name='minus_di-enabled'),
            Categorical(['buy_signal'], name='trigger')
        ]

    @staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:
        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            conditions = []

            # GUARDS AND TRENDS
            if params.get('sell-adx-enabled'):
                conditions.append(dataframe['sell-adx'] > params['sell-adx-value'])
            if params.get('sell-plus-enabled'):
                conditions.append(dataframe['sell-plus_di'] > params['sell-plus_di-value'])
            if params.get('sell-minus-enabled'):
                conditions.append(dataframe['sell-minus_di'] > params['sell-minus_di-value'])


            # TRIGGERS
            if 'sell-trigger' in params:
                if params['sell-trigger'] == 'sell_signal':
                    conditions.append(qtpylib.crossed_above(dataframe['sell-plus_di'], dataframe['sell-minus_di']))

            conditions.append(dataframe['volume'] > 0)

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell'] = 1

            return dataframe
        return populate_sell_trend

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:
        return [
            Integer(0, 50, name='sell-adx-value'),
            Integer(0, 40, name='sell-plus_di-value'),
            Integer(0, 40, name='sell-minus_di-value'),
            Categorical([True, False], name='sell-adx-enabled'),
            Categorical([True, False], name='sell-plus_di-enabled'),
            Categorical([True, False], name='sell-minus_di-enabled'),
            Categorical(['sell_signal'], name='sell-trigger')
        ]
      
