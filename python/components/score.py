import asyncio
import datetime
from typing import List, Union, Tuple
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


class Score():
  def __init__(self):
    '''
    スコア指標
     - 最大電流値
     - 非線形性
     - キャパシタ容量 + メモリ特性
    '''
    pass


  async def all(self, data: List[List[Union[datetime.datetime, float]]]):
    task = [
      self.current(data),
      self.nonlinearity(data),
      self.hysteresis(data)
    ]
    score1, score2, score3 = asyncio.gather(*task)

    # score1~3を真相学習モデル(各タスクごと)に通し、total_scoreを算出する
  

  async def current(self, data: List[List[Union[datetime.datetime, float]]]) -> Tuple[str, float]:
    # データを整形する
    df = self.arrange(data)

    # 'voltage_ai{i}'カラムの最大電流値とそのカラム名を取得
    voltage_columns = [col for col in df.columns if col.startswith('voltage_ai')]
    max_column = df[voltage_columns].max().idxmax()  # 最大値を持つカラム名を取得
    max_current = df[max_column].max()               # そのカラムの最大値を取得

    return max_column, float(max_current)


  async def nonlinearity(self, data: List[List[Union[datetime.datetime, float]]]) -> Tuple[str, float]:
    # データを整形
    df = self.arrange(data)

    # 'current_ai{i}'カラムのみを対象とする
    current_columns = [col for col in df.columns if col.startswith('current_ai')]

    # 電圧の最小値と最大値を取得
    voltage_min = df['voltage'].min()
    voltage_max = df['voltage'].max()

    # 非線形性スコアを保存するリスト
    scores = []

    # 各カラムに対してスコアリングを実施
    for column in current_columns:
      voltage = df['voltage'].values  # 電圧データ
      current = df[column].values     # 電流データ

      # 電圧範囲の10%地点と90%地点を計算
      voltage_10_percent = voltage_min + 0.1 * (voltage_max - voltage_min)
      voltage_90_percent = voltage_min + 0.9 * (voltage_max - voltage_min)

      # 補間関数を使って、10%と90%地点での電流を推定
      interp_func = interp1d(voltage, current, kind='linear', fill_value="extrapolate")
      current_10_percent = interp_func(voltage_10_percent)
      current_90_percent = interp_func(voltage_90_percent)

      # 10%地点と90%地点での微分（線形近似としての傾き）を計算
      slope_10_percent = (current_90_percent - current_10_percent) / (voltage_90_percent - voltage_10_percent)

      # 微分の結果（傾き）の交点を求める
      intercept = voltage_10_percent - (current_10_percent / slope_10_percent)

      # 交点の電圧をmax電圧で規格化
      normalized_intercept = intercept / voltage_max if voltage_max != 0 else 0

      # スコアとして保存
      scores.append((column, normalized_intercept))

    # 最もスコアが高いカラムを選択
    max_column, max_score = max(scores, key=lambda x: x[1])

    return max_column, float(max_score)



  async def hysteresis(self, data: List[List[Union[datetime.datetime, float]]]) -> Tuple[str, float]:
    '''
    キャパシタ成分とヒステリシス成分の両方
    '''
    # データを整形
    df = self.arrange(data)

    # 'current_ai{i}'カラムのみを対象とする
    current_columns = [col for col in df.columns if col.startswith('current_ai')]

    # 電圧の最小値と最大値を取得
    voltage_min = df['voltage'].min()
    voltage_max = df['voltage'].max()

    # 0.01Vごとに電圧点を生成
    voltage_points = np.arange(voltage_min, voltage_max, 0.01)

    # ヒステリシススコアを保存するリスト
    scores = []

    # 各カラムに対してスコアリングを実施
    for column in current_columns:
      voltage = df['voltage'].values  # 電圧データ
      current = df[column].values     # 電流データ

      # 行きと帰りのデータを作るための補間関数を生成
      forward_interp = interp1d(voltage, current, kind='linear', fill_value="extrapolate")
      backward_interp = interp1d(voltage[::-1], current[::-1], kind='linear', fill_value="extrapolate")

      max_diff = 0  # ヒステリシスの最大の開き

      # 0.01Vごとの電圧点でヒステリシスを評価
      for v_point in voltage_points:
        # 補間によって行きと帰りの電流値を取得
        forward_current = forward_interp(v_point)
        backward_current = backward_interp(v_point)

        # 帰りの電流の絶対値が大きい場合のみ評価
        if abs(backward_current) > abs(forward_current):
          # ヒステリシスの差を計算
          diff = abs(backward_current - forward_current)
          max_diff = max(max_diff, diff)

      # スコアとして保存
      scores.append((column, max_diff))

    # 最もスコアが高いカラムを選択
    max_column, max_score = max(scores, key=lambda x: x[1])

    return max_column, float(max_score)


  
  async def arrange(self, data: List[List[Union[datetime.datetime, float]]]) -> pd.DataFrame:
    # カラム名を定義（'voltage'カラムを含める）
    column_names = ['timestamp', 'elapsed_time', 'voltage'] + [f'current_ai{i}' for i in range(len(data[0]) - 3)]

    # データフレームを作成
    df = pd.DataFrame(data, columns=column_names)

    # 時間でソートしておく
    df = df.sort_values(by='elapsed_time').reset_index(drop=True)

    return df
