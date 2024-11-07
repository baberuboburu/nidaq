import pandas as pd
import numpy as np
import datetime
from typing import List, Union


class Optimize():
  def __init__(self):
    '''
    解析指標
     - 最大電流値
     - 非線形性
     - キャパシタ容量 + メモリ特性
    '''
    pass


  async def main(self, data: List[List[Union[datetime.datetime, float]]], optimize: str):
    df = await self.arrange(data)
    score = await self.routing(df, optimize)
    return
  

  async def arrange(self, data: List[List[Union[datetime.datetime, float]]]) -> pd.DataFrame:
    column_names = ['timestamp', 'elapsed_time'] + [f'voltage_ai{i}' for i in range(len(data[0]) - 2)]
    df = pd.DataFrame(data, columns=column_names)
    print(df.head())

    return df
  

  async def routing(self, df: pd.DataFrame, optimize: str):
    if optimize == 'current':
      return await self.current(df)
    elif optimize == 'capacitance':
      return await self.capacitance(df)
    elif optimize == 'nonlinearity':
      return await self.nonlinearity(df)
    elif optimize == 'histeresis':
      return await self.histeresis(df)
    else:
      raise ValueError(f'optimize変数が正しく設定されていません。\n指定されたoptimize変数: {optimize}')
  

  async def current(self):
    return
  

  async def capacitance(self):
    return
  

  async def nonlinearity(self):
    return

  
  async def histeresis(self):
    return