import pandas as pd
import numpy as np
import datetime
from typing import List, Union


class SideGate():
  def __init__(self):
    '''
    解析指標
     - 最大電流値
     - 非線形性
     - キャパシタ容量 + メモリ特性
    '''
    pass


  async def all(self, data: List[List[Union[datetime.datetime, float]]], optimize: str):
    return
  

  async def is_sidegate(self, data: List[List[Union[datetime.datetime, float]]]) -> bool:
    '''
    サイドゲート効果があるかどうかを判定する関数
    '''
    # データを整形する
    df = self.arrange(data)

    # 2つの電圧を足した時のIV特性と、それぞれの電圧におけるIV特性の和が、非線形的に変化しているかを確認する

    return
  

  async def voltage(self, data: List[List[Union[datetime.datetime, float]]]):
    '''
    電圧依存性に対する最適化
    ・履歴効果
      - 参照電圧: 0V~+3Vで、0.01VずつのDCを印加し、それに対するヒステリシスの影響をDBに保存しておく。
    ・非線形性
      - 
    '''
    # データを整形する
    df = self.arrange(data)

    # 各電圧におけるヒステリシスを評価し、ヒステリシス変化が最も大きい電圧点を算出する

    # 非線形性のスコアを算出する

    async def hysteresis(df: pd.DataFrame) -> List[float, float]:
      '''
      ヒステリシスが、サイドゲート効果によってどのくらい変化するか算出する関数。
      dfを受け取り、「変化が最大となる電圧」と「その電圧における差」を返却する。
      '''
      return

    async def nonlinearity(df: pd.DataFrame) -> List[float, float]:
      '''
      非線形性が、サイドゲート効果によってどのくらい変化するか算出する関数。
      dfを受け取り、「非線形性が最大となる電圧」と「その電圧におけるスコア」を返却する。
      '''
      return

    return
  

  async def frequency(self):
    '''
    周波数に対する最適化
    とりあえずこの関数は定義しないで、低周波数(キャパシタ容量が現れないくらい遅い測定)にのみ焦点を当てる。
    '''
    return
  

  async def arrange(self, data: List[List[Union[datetime.datetime, float]]]) -> pd.DataFrame:
    column_names = ['timestamp', 'elapsed_time'] + [f'voltage_ai{i}' for i in range(len(data[0]) - 2)]
    df = pd.DataFrame(data, columns=column_names)
    print(df.head())

    return df